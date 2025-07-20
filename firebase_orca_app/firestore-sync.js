/**
 * Firestore Sync Service
 * Syncs whale sighting data from external sources to Firestore collections
 * Makes data accessible to map configuration objects and real-time queries
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');

class FirestoreSync {
    constructor() {
        this.initialized = false;
        this.collections = {
            sightings: 'whale_sightings',
            importStatus: 'import_status',
            mapData: 'map_data_cache'
        };
        
        this.initializeFirestore();
    }

    /**
     * Initialize Firebase Admin SDK
     */
    initializeFirestore() {
        try {
            // Check if Firebase is already initialized
            if (admin.apps.length === 0) {
                // Require service account key for production use
                const serviceAccountPath = path.join(__dirname, 'config/serviceAccountKey.json');
                
                if (!fs.existsSync(serviceAccountPath)) {
                    throw new Error(`Service account key not found at ${serviceAccountPath}. Please download from Google Cloud Console and place it there.`);
                }
                
                const serviceAccount = JSON.parse(fs.readFileSync(serviceAccountPath, 'utf8'));
                
                admin.initializeApp({
                    credential: admin.credential.cert(serviceAccount),
                    databaseURL: process.env.FIREBASE_DATABASE_URL || `https://${serviceAccount.project_id}-default-rtdb.firebaseio.com`
                });
                
                console.log('🔥 Firebase Admin SDK initialized with service account');
            }
            
            this.db = admin.firestore();
            this.initialized = true;
            
            console.log('✅ Firestore connection established');
            
        } catch (error) {
            console.error('❌ Firestore initialization REQUIRED but failed:', error.message);
            console.error('📝 Please follow setup instructions to enable Firestore API and add service account key');
            throw error; // Don't fall back - require proper setup
        }
    }

    /**
     * Sync whale sightings data to Firestore
     */
    async syncSightingsData(sightingsData) {
        if (!this.initialized) {
            throw new Error('Firestore not initialized - please enable Firestore API and configure service account');
        }

        try {
            const batch = this.db.batch();
            let syncedCount = 0;
            const timestamp = new Date();

            console.log(`🔄 Syncing ${sightingsData.length} sightings to Firestore...`);

            for (const sighting of sightingsData) {
                const docId = this.generateSightingId(sighting);
                const docRef = this.db.collection(this.collections.sightings).doc(docId);
                
                const firestoreData = this.formatSightingForFirestore(sighting, timestamp);
                batch.set(docRef, firestoreData, { merge: true });
                syncedCount++;
            }

            // Add batch metadata
            const metadataRef = this.db.collection(this.collections.sightings).doc('_metadata');
            batch.set(metadataRef, {
                lastSync: timestamp,
                totalSightings: sightingsData.length,
                syncedCount,
                sources: this.extractUniqueSources(sightingsData),
                dataVersion: this.generateDataVersion()
            }, { merge: true });

            await batch.commit();

            console.log(`✅ Successfully synced ${syncedCount} sightings to Firestore`);
            
            // Update map data cache
            await this.updateMapDataCache(sightingsData);

            return { success: true, synced: syncedCount, mode: 'firestore' };

        } catch (error) {
            console.error('❌ Firestore sync failed:', error);
            throw error;
        }
    }

    /**
     * Generate consistent document ID for sighting
     */
    generateSightingId(sighting) {
        // Use existing ID if available, otherwise generate from timestamp + location + source
        if (sighting.id) {
            return sighting.id.replace(/[^a-zA-Z0-9_-]/g, '_');
        }
        
        const timestamp = new Date(sighting.timestamp).getTime();
        const location = (sighting.location || 'unknown').replace(/[^a-zA-Z0-9]/g, '_');
        const source = (sighting.source || 'unknown').replace(/[^a-zA-Z0-9]/g, '_');
        
        return `${timestamp}_${location}_${source}_${Math.random().toString(36).substr(2, 6)}`;
    }

    /**
     * Format sighting data for Firestore storage
     */
    formatSightingForFirestore(sighting, syncTimestamp) {
        return {
            // Core sighting data
            timestamp: admin.firestore.Timestamp.fromDate(new Date(sighting.timestamp)),
            location: sighting.location || 'Unknown',
            coordinates: sighting.coordinates ? {
                lat: parseFloat(sighting.coordinates.lat) || 0,
                lng: parseFloat(sighting.coordinates.lng) || 0
            } : null,
            groupSize: parseInt(sighting.groupSize) || 1,
            behavior: sighting.behavior || 'unknown',
            confidence: parseFloat(sighting.confidence) || 0.5,
            
            // Source information
            source: sighting.source || 'Unknown',
            sourceType: sighting.sourceType || 'unknown',
            podIdentification: sighting.podIdentification || null,
            
            // Additional metadata
            platform: sighting.platform || null,
            originalText: sighting.originalText || null,
            node: sighting.node || null,
            detectionCount: parseInt(sighting.detectionCount) || null,
            
            // Firestore metadata
            syncedAt: admin.firestore.Timestamp.fromDate(syncTimestamp),
            dataVersion: this.generateDataVersion(),
            
            // Map configuration fields
            mapReady: true,
            geoHash: this.generateGeoHash(sighting.coordinates),
            timeSlot: this.getTimeSlot(new Date(sighting.timestamp)),
            
            // Search and filtering
            searchTags: this.generateSearchTags(sighting),
            behaviorCategory: this.categorizeBehavior(sighting.behavior),
            confidenceLevel: this.categorizeConfidence(sighting.confidence)
        };
    }

    /**
     * Generate geohash for spatial indexing
     */
    generateGeoHash(coordinates) {
        if (!coordinates || !coordinates.lat || !coordinates.lng) return null;
        
        // Simple geohash implementation (you might want to use a proper library)
        const lat = parseFloat(coordinates.lat);
        const lng = parseFloat(coordinates.lng);
        
        return `${Math.floor(lat * 100)}_${Math.floor(lng * 100)}`;
    }

    /**
     * Get time slot for temporal indexing
     */
    getTimeSlot(date) {
        const hour = date.getHours();
        
        if (hour >= 5 && hour < 9) return 'dawn';
        if (hour >= 9 && hour < 12) return 'morning';
        if (hour >= 12 && hour < 17) return 'afternoon';
        if (hour >= 17 && hour < 20) return 'dusk';
        return 'night';
    }

    /**
     * Generate search tags for full-text search
     */
    generateSearchTags(sighting) {
        const tags = [];
        
        if (sighting.location) tags.push(sighting.location.toLowerCase());
        if (sighting.behavior) tags.push(sighting.behavior.toLowerCase());
        if (sighting.podIdentification) tags.push(sighting.podIdentification.toLowerCase());
        if (sighting.source) tags.push(sighting.source.toLowerCase());
        
        return tags;
    }

    /**
     * Categorize behavior for filtering
     */
    categorizeBehavior(behavior) {
        const behaviorLower = (behavior || '').toLowerCase();
        
        if (behaviorLower.includes('forag') || behaviorLower.includes('feed')) return 'feeding';
        if (behaviorLower.includes('travel') || behaviorLower.includes('transit')) return 'traveling';
        if (behaviorLower.includes('social') || behaviorLower.includes('play')) return 'social';
        if (behaviorLower.includes('rest') || behaviorLower.includes('mill')) return 'resting';
        
        return 'unknown';
    }

    /**
     * Categorize confidence level
     */
    categorizeConfidence(confidence) {
        const conf = parseFloat(confidence) || 0;
        
        if (conf >= 0.8) return 'high';
        if (conf >= 0.6) return 'medium';
        if (conf >= 0.4) return 'low';
        return 'very_low';
    }

    /**
     * Update map data cache for quick access
     */
    async updateMapDataCache(sightingsData) {
        if (!this.initialized) {
            throw new Error('Firestore not initialized - cannot update map data cache');
        }

        try {
            // Generate map configuration data
            const mapData = {
                lastUpdated: admin.firestore.Timestamp.now(),
                totalSightings: sightingsData.length,
                
                // Hotspot analysis
                hotspots: this.generateHotspots(sightingsData),
                
                // Temporal patterns
                hourlyDistribution: this.analyzeHourlyDistribution(sightingsData),
                weeklyPatterns: this.analyzeWeeklyPatterns(sightingsData),
                
                // Source breakdown
                sourceStats: this.analyzeSourceStats(sightingsData),
                
                // Behavior patterns
                behaviorDistribution: this.analyzeBehaviorDistribution(sightingsData),
                
                // Geographic bounds
                bounds: this.calculateGeographicBounds(sightingsData),
                
                // Recent activity (last 7 days)
                recentActivity: this.getRecentActivity(sightingsData, 7)
            };

            await this.db.collection(this.collections.mapData).doc('current').set(mapData);
            console.log('✅ Map data cache updated');

        } catch (error) {
            console.error('❌ Failed to update map data cache:', error);
            throw error;
        }
    }

    /**
     * Generate hotspot data for map overlays
     */
    generateHotspots(sightingsData) {
        const locationCounts = {};
        
        sightingsData.forEach(sighting => {
            const location = sighting.location || 'Unknown';
            if (!locationCounts[location]) {
                locationCounts[location] = {
                    name: location,
                    coordinates: sighting.coordinates,
                    count: 0,
                    totalGroupSize: 0,
                    behaviors: {},
                    sources: {}
                };
            }
            
            locationCounts[location].count++;
            locationCounts[location].totalGroupSize += sighting.groupSize || 0;
            
            const behavior = sighting.behavior || 'unknown';
            locationCounts[location].behaviors[behavior] = (locationCounts[location].behaviors[behavior] || 0) + 1;
            
            const source = sighting.source || 'Unknown';
            locationCounts[location].sources[source] = (locationCounts[location].sources[source] || 0) + 1;
        });
        
        return Object.values(locationCounts)
            .filter(hotspot => hotspot.coordinates)
            .map(hotspot => ({
                ...hotspot,
                intensity: Math.min(1.0, hotspot.count / 10),
                avgGroupSize: Math.round(hotspot.totalGroupSize / hotspot.count * 10) / 10,
                dominantBehavior: Object.keys(hotspot.behaviors).reduce((a, b) => 
                    hotspot.behaviors[a] > hotspot.behaviors[b] ? a : b, 'unknown')
            }))
            .sort((a, b) => b.count - a.count);
    }

    /**
     * Analyze hourly distribution patterns
     */
    analyzeHourlyDistribution(sightingsData) {
        const hourly = new Array(24).fill(0);
        
        sightingsData.forEach(sighting => {
            const hour = new Date(sighting.timestamp).getHours();
            hourly[hour]++;
        });
        
        return hourly;
    }

    /**
     * Analyze weekly patterns
     */
    analyzeWeeklyPatterns(sightingsData) {
        const weekly = new Array(7).fill(0);
        const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        
        sightingsData.forEach(sighting => {
            const day = new Date(sighting.timestamp).getDay();
            weekly[day]++;
        });
        
        return weekly.map((count, index) => ({
            day: dayNames[index],
            count
        }));
    }

    /**
     * Analyze source statistics
     */
    analyzeSourceStats(sightingsData) {
        const sourceStats = {};
        
        sightingsData.forEach(sighting => {
            const source = sighting.source || 'Unknown';
            if (!sourceStats[source]) {
                sourceStats[source] = {
                    count: 0,
                    avgConfidence: 0,
                    totalConfidence: 0
                };
            }
            
            sourceStats[source].count++;
            sourceStats[source].totalConfidence += sighting.confidence || 0;
            sourceStats[source].avgConfidence = sourceStats[source].totalConfidence / sourceStats[source].count;
        });
        
        return sourceStats;
    }

    /**
     * Analyze behavior distribution
     */
    analyzeBehaviorDistribution(sightingsData) {
        const behaviors = {};
        
        sightingsData.forEach(sighting => {
            const behavior = sighting.behavior || 'unknown';
            behaviors[behavior] = (behaviors[behavior] || 0) + 1;
        });
        
        return behaviors;
    }

    /**
     * Calculate geographic bounds
     */
    calculateGeographicBounds(sightingsData) {
        let minLat = 90, maxLat = -90, minLng = 180, maxLng = -180;
        let validCoords = 0;
        
        sightingsData.forEach(sighting => {
            if (sighting.coordinates && sighting.coordinates.lat && sighting.coordinates.lng) {
                const lat = parseFloat(sighting.coordinates.lat);
                const lng = parseFloat(sighting.coordinates.lng);
                
                if (!isNaN(lat) && !isNaN(lng)) {
                    minLat = Math.min(minLat, lat);
                    maxLat = Math.max(maxLat, lat);
                    minLng = Math.min(minLng, lng);
                    maxLng = Math.max(maxLng, lng);
                    validCoords++;
                }
            }
        });
        
        if (validCoords === 0) {
            // Default to Salish Sea area
            return {
                north: 49.0,
                south: 47.5,
                east: -122.0,
                west: -124.0,
                center: { lat: 48.25, lng: -123.0 }
            };
        }
        
        return {
            north: maxLat,
            south: minLat,
            east: maxLng,
            west: minLng,
            center: {
                lat: (minLat + maxLat) / 2,
                lng: (minLng + maxLng) / 2
            }
        };
    }

    /**
     * Get recent activity
     */
    getRecentActivity(sightingsData, days) {
        const cutoff = new Date(Date.now() - (days * 24 * 60 * 60 * 1000));
        
        return sightingsData
            .filter(sighting => new Date(sighting.timestamp) > cutoff)
            .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    }

    /**
     * Extract unique sources
     */
    extractUniqueSources(sightingsData) {
        return [...new Set(sightingsData.map(s => s.source || 'Unknown'))];
    }

    /**
     * Generate data version
     */
    generateDataVersion() {
        return `v${Date.now()}`;
    }

    /**
     * Sync import status to Firestore
     */
    async syncImportStatus(importResults) {
        if (!this.initialized) {
            throw new Error('Firestore not initialized - cannot sync import status');
        }

        try {
            await this.db.collection(this.collections.importStatus).doc('latest').set({
                ...importResults,
                timestamp: admin.firestore.Timestamp.fromDate(new Date(importResults.timestamp))
            });

            console.log('✅ Import status synced to Firestore');
        } catch (error) {
            console.error('❌ Failed to sync import status:', error);
            throw error;
        }
    }

    /**
     * Get sightings for map configuration
     */
    async getSightingsForMap(timeRange = null, bounds = null) {
        if (!this.initialized) {
            throw new Error('Firestore not initialized - please enable Firestore API and configure service account');
        }

        try {
            let query = this.db.collection(this.collections.sightings)
                .where('mapReady', '==', true)
                .orderBy('timestamp', 'desc')
                .limit(1000);

            // Add time range filter if specified
            if (timeRange && timeRange.start && timeRange.end) {
                query = query
                    .where('timestamp', '>=', admin.firestore.Timestamp.fromDate(new Date(timeRange.start)))
                    .where('timestamp', '<=', admin.firestore.Timestamp.fromDate(new Date(timeRange.end)));
            }

            const snapshot = await query.get();
            const sightings = [];

            snapshot.forEach(doc => {
                const data = doc.data();
                sightings.push({
                    id: doc.id,
                    ...data,
                    timestamp: data.timestamp.toDate().toISOString()
                });
            });

            // Get cached map data
            const mapDataDoc = await this.db.collection(this.collections.mapData).doc('current').get();
            const mapData = mapDataDoc.exists ? mapDataDoc.data() : {};

            return {
                sightings,
                hotspots: mapData.hotspots || [],
                bounds: mapData.bounds || null,
                lastUpdated: mapData.lastUpdated ? mapData.lastUpdated.toDate().toISOString() : null
            };

        } catch (error) {
            console.error('❌ Failed to get map sightings from Firestore:', error);
            throw error;
        }
    }

    /**
     * Check if Firestore is available
     */
    isAvailable() {
        return this.initialized;
    }
}

module.exports = FirestoreSync; 