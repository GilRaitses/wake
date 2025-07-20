/**
 * BlueSky Feed Importer
 * Fetches whale sightings from Orca Behavior Institute's BlueSky feed
 * Processes posts from @orcabehaviorinstitute.org for real-time sightings
 */

const fs = require('fs');
const path = require('path');

class BlueSkyImporter {
    constructor() {
        this.profileHandle = 'orcabehaviorinstitute.org';
        this.feedId = 'aaaivu343h5ge';
        this.baseUrl = 'https://bsky.app';
        this.apiUrl = 'https://bsky.social/xrpc';
        this.dataFile = path.join(__dirname, '../data/bluesky_sightings.json');
        this.lastImportFile = path.join(__dirname, '../data/last_bluesky_import.json');
        
        // Location mapping from common terms
        this.locationMap = {
            'haro strait': { name: 'Haro Strait', coordinates: { lat: 48.5, lng: -123.2 } },
            'lime kiln': { name: 'Lime Kiln Point', coordinates: { lat: 48.516, lng: -123.152 } },
            'boundary pass': { name: 'Boundary Pass', coordinates: { lat: 48.7, lng: -123.0 } },
            'san juan channel': { name: 'San Juan Channel', coordinates: { lat: 48.55, lng: -123.05 } },
            'rosario strait': { name: 'Rosario Strait', coordinates: { lat: 48.65, lng: -122.7 } },
            'deception pass': { name: 'Deception Pass', coordinates: { lat: 48.4, lng: -122.6 } },
            'puget sound': { name: 'Puget Sound', coordinates: { lat: 47.6, lng: -122.3 } },
            'elliott bay': { name: 'Elliott Bay', coordinates: { lat: 47.6, lng: -122.35 } },
            'admiralty inlet': { name: 'Admiralty Inlet', coordinates: { lat: 48.15, lng: -122.75 } },
            'port townsend': { name: 'Port Townsend', coordinates: { lat: 48.1, lng: -122.8 } },
            'friday harbor': { name: 'Friday Harbor', coordinates: { lat: 48.54, lng: -123.01 } },
            'false bay': { name: 'False Bay', coordinates: { lat: 48.48, lng: -123.05 } },
            'cattle point': { name: 'Cattle Point', coordinates: { lat: 48.45, lng: -122.95 } }
        };
        
        // Pod identification patterns
        this.podPatterns = {
            'j pod': 'J Pod',
            'j-pod': 'J Pod',
            'k pod': 'K Pod', 
            'k-pod': 'K Pod',
            'l pod': 'L Pod',
            'l-pod': 'L Pod',
            't65a': 'T65A Pod',
            't137': 'T137 Pod',
            't49a': 'T49A Pod',
            't36a': 'T36A Pod'
        };
    }

    /**
     * Import sightings from BlueSky feed
     */
    async importSightings() {
        console.log('🐦 Starting BlueSky feed import...');
        
        try {
            // Try different methods to get feed data
            let feedData = null;
            
            // Method 1: Try AT Protocol API
            feedData = await this.fetchViaATProto();
            
            // Method 2: Try web scraping if API fails
            if (!feedData) {
                console.log('📄 API failed, trying web scraping...');
                feedData = await this.scrapeFeedPage();
            }
            
            if (!feedData) {
                throw new Error('Could not fetch BlueSky feed data');
            }
            
            // Process and extract sightings
            const sightings = this.processFeedPosts(feedData);
            
            // Save to file
            await this.saveSightings(sightings);
            
            // Update last import
            await this.updateLastImport();
            
            console.log(`✅ Successfully imported ${sightings.length} BlueSky sightings`);
            return sightings;
            
        } catch (error) {
            console.error('❌ BlueSky import failed:', error);
            
            // Return mock data if import fails
            return this.generateMockBlueSkyData();
        }
    }

    /**
     * Fetch via AT Protocol API
     */
    async fetchViaATProto() {
        try {
            const fetch = (await import('node-fetch')).default;
            
            // Get profile DID
            const profileUrl = `${this.apiUrl}/com.atproto.identity.resolveHandle?handle=${this.profileHandle}`;
            const profileResponse = await fetch(profileUrl);
            const profileData = await profileResponse.json();
            
            if (!profileData.did) {
                throw new Error('Could not resolve profile DID');
            }
            
            // Get feed posts
            const feedUrl = `${this.apiUrl}/com.atproto.repo.listRecords?repo=${profileData.did}&collection=app.bsky.feed.post&limit=50`;
            const feedResponse = await fetch(feedUrl);
            const feedData = await feedResponse.json();
            
            return feedData.records || [];
            
        } catch (error) {
            console.log('AT Protocol API failed:', error.message);
            return null;
        }
    }

    /**
     * Scrape feed page for posts
     */
    async scrapeFeedPage() {
        try {
            const fetch = (await import('node-fetch')).default;
            
            const feedUrl = `${this.baseUrl}/profile/${this.profileHandle}/feed/${this.feedId}`;
            const response = await fetch(feedUrl, {
                headers: {
                    'User-Agent': 'ORCAST-Data-Importer/1.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }
            });
            
            const html = await response.text();
            
            // Extract JSON data from script tags
            const scriptMatches = html.match(/<script[^>]*>(.*?)<\/script>/gs);
            
            for (const script of scriptMatches || []) {
                // Look for feed data in various formats
                const feedMatch = script.match(/"posts":\s*(\[.*?\])/s) ||
                                script.match(/"feed":\s*(\[.*?\])/s) ||
                                script.match(/"records":\s*(\[.*?\])/s);
                
                if (feedMatch) {
                    try {
                        return JSON.parse(feedMatch[1]);
                    } catch (e) {
                        continue;
                    }
                }
            }
            
            return null;
            
        } catch (error) {
            console.error('Feed scraping failed:', error);
            return null;
        }
    }

    /**
     * Process feed posts to extract whale sightings
     */
    processFeedPosts(posts) {
        const sightings = [];
        
        for (const post of posts) {
            const sighting = this.extractSightingFromPost(post);
            if (sighting) {
                sightings.push(sighting);
            }
        }
        
        return sightings.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    }

    /**
     * Extract sighting information from a single post
     */
    extractSightingFromPost(post) {
        let text = '';
        let timestamp = new Date().toISOString();
        
        // Handle different post structures
        if (post.value && post.value.text) {
            text = post.value.text;
            timestamp = post.value.createdAt || post.createdAt || timestamp;
        } else if (post.record && post.record.text) {
            text = post.record.text;
            timestamp = post.record.createdAt || timestamp;
        } else if (post.text) {
            text = post.text;
            timestamp = post.createdAt || timestamp;
        }
        
        if (!text) return null;
        
        const lowerText = text.toLowerCase();
        
        // Look for whale/orca related keywords
        const whaleKeywords = ['orca', 'whale', 'srkw', 'killer whale', 'pod', 'j pod', 'k pod', 'l pod'];
        const hasWhaleContent = whaleKeywords.some(keyword => lowerText.includes(keyword));
        
        if (!hasWhaleContent) return null;
        
        // Extract location
        const location = this.extractLocation(text);
        
        // Extract pod information
        const podId = this.extractPodId(text);
        
        // Extract group size
        const groupSize = this.extractGroupSize(text);
        
        // Extract behavior
        const behavior = this.extractBehavior(text);
        
        // Extract time information
        const timeInfo = this.extractTimeInfo(text, timestamp);
        
        return {
            id: `bluesky_${post.uri || post.cid || Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            timestamp: timeInfo.timestamp,
            location: location.name,
            coordinates: location.coordinates,
            groupSize: groupSize,
            podIdentification: podId,
            behavior: behavior,
            confidence: this.calculateConfidence(text, location, podId),
            source: 'Orca Behavior Institute (BlueSky)',
            sourceType: 'social_media_report',
            originalText: text,
            platform: 'BlueSky',
            author: this.profileHandle,
            postId: post.uri || post.cid,
            originalData: post
        };
    }

    /**
     * Extract location from post text
     */
    extractLocation(text) {
        const lowerText = text.toLowerCase();
        
        // Check for known locations
        for (const [key, location] of Object.entries(this.locationMap)) {
            if (lowerText.includes(key)) {
                return location;
            }
        }
        
        // Look for coordinate patterns
        const coordMatch = text.match(/(\d+\.\d+)[,\s]+(-?\d+\.\d+)/);
        if (coordMatch) {
            return {
                name: 'GPS Coordinates',
                coordinates: { lat: parseFloat(coordMatch[1]), lng: parseFloat(coordMatch[2]) }
            };
        }
        
        // Default to general area
        return {
            name: 'Salish Sea',
            coordinates: { lat: 48.5, lng: -123.0 }
        };
    }

    /**
     * Extract pod identification
     */
    extractPodId(text) {
        const lowerText = text.toLowerCase();
        
        for (const [pattern, podName] of Object.entries(this.podPatterns)) {
            if (lowerText.includes(pattern)) {
                return podName;
            }
        }
        
        // Look for individual whale IDs
        const whaleIdMatch = text.match(/[jklts]\d+[a-z]?/gi);
        if (whaleIdMatch) {
            return whaleIdMatch[0].toUpperCase();
        }
        
        return null;
    }

    /**
     * Extract group size from text
     */
    extractGroupSize(text) {
        // Look for explicit numbers
        const numberMatch = text.match(/(\d+)\s*(?:orcas?|whales?|individuals?)/i);
        if (numberMatch) {
            return parseInt(numberMatch[1]);
        }
        
        // Look for descriptive terms
        const lowerText = text.toLowerCase();
        if (lowerText.includes('pod')) return 8; // Average pod size
        if (lowerText.includes('family')) return 4;
        if (lowerText.includes('group')) return 3;
        if (lowerText.includes('pair')) return 2;
        if (lowerText.includes('single') || lowerText.includes('lone')) return 1;
        
        // Default
        return 4;
    }

    /**
     * Extract behavior from text
     */
    extractBehavior(text) {
        const lowerText = text.toLowerCase();
        
        if (lowerText.includes('forag') || lowerText.includes('feed') || lowerText.includes('hunt')) return 'foraging';
        if (lowerText.includes('travel') || lowerText.includes('transit') || lowerText.includes('passage')) return 'traveling';
        if (lowerText.includes('social') || lowerText.includes('play') || lowerText.includes('breach')) return 'socializing';
        if (lowerText.includes('rest') || lowerText.includes('mill') || lowerText.includes('slow')) return 'resting';
        if (lowerText.includes('call') || lowerText.includes('vocal') || lowerText.includes('echolocation')) return 'socializing';
        
        return 'unknown';
    }

    /**
     * Extract time information
     */
    extractTimeInfo(text, defaultTimestamp) {
        // Look for time references in text
        const timeMatch = text.match(/(\d{1,2}):(\d{2})\s*(am|pm)?/i);
        const dateMatch = text.match(/(\d{1,2})\/(\d{1,2})(?:\/(\d{2,4}))?/);
        
        let timestamp = new Date(defaultTimestamp);
        
        if (timeMatch) {
            let hour = parseInt(timeMatch[1]);
            const minute = parseInt(timeMatch[2]);
            const ampm = timeMatch[3];
            
            if (ampm && ampm.toLowerCase() === 'pm' && hour !== 12) hour += 12;
            if (ampm && ampm.toLowerCase() === 'am' && hour === 12) hour = 0;
            
            timestamp.setHours(hour, minute, 0, 0);
        }
        
        if (dateMatch) {
            const month = parseInt(dateMatch[1]) - 1; // JS months are 0-indexed
            const day = parseInt(dateMatch[2]);
            let year = dateMatch[3] ? parseInt(dateMatch[3]) : timestamp.getFullYear();
            
            if (year < 100) year += 2000; // Convert 2-digit years
            
            timestamp.setFullYear(year, month, day);
        }
        
        return {
            timestamp: timestamp.toISOString()
        };
    }

    /**
     * Calculate confidence score
     */
    calculateConfidence(text, location, podId) {
        let confidence = 0.6; // Base confidence for social media
        
        // Boost for specific details
        if (podId) confidence += 0.15;
        if (location.name !== 'Salish Sea') confidence += 0.1; // Specific location
        if (text.includes('photo') || text.includes('video')) confidence += 0.1;
        if (text.includes('confirmed') || text.includes('verified')) confidence += 0.1;
        if (text.match(/\d+:\d+/)) confidence += 0.05; // Specific time
        
        // Reduce for uncertain language
        if (text.includes('possible') || text.includes('maybe')) confidence -= 0.1;
        if (text.includes('unconfirmed')) confidence -= 0.15;
        
        return Math.max(0.3, Math.min(0.95, confidence));
    }

    /**
     * Save sightings to file
     */
    async saveSightings(sightings) {
        const data = {
            lastUpdated: new Date().toISOString(),
            source: 'Orca Behavior Institute BlueSky Feed',
            totalSightings: sightings.length,
            blueskySightings: sightings
        };
        
        fs.writeFileSync(this.dataFile, JSON.stringify(data, null, 2));
        console.log(`💾 Saved ${sightings.length} BlueSky sightings to ${this.dataFile}`);
    }

    /**
     * Update last import timestamp
     */
    async updateLastImport() {
        const importInfo = {
            lastImport: new Date().toISOString(),
            source: 'BlueSky',
            status: 'success'
        };
        
        fs.writeFileSync(this.lastImportFile, JSON.stringify(importInfo, null, 2));
    }

    /**
     * Generate mock BlueSky data for testing
     */
    generateMockBlueSkyData() {
        const mockSightings = [];
        const locations = Object.values(this.locationMap);
        const behaviors = ['foraging', 'traveling', 'socializing', 'resting'];
        const pods = Object.values(this.podPatterns);
        
        for (let i = 0; i < 20; i++) {
            const location = locations[Math.floor(Math.random() * locations.length)];
            const daysAgo = Math.floor(Math.random() * 7); // Last week
            const timestamp = new Date(Date.now() - (daysAgo * 24 * 60 * 60 * 1000));
            
            mockSightings.push({
                id: `mock_bluesky_${i}`,
                timestamp: timestamp.toISOString(),
                location: location.name,
                coordinates: location.coordinates,
                groupSize: Math.floor(Math.random() * 8) + 1,
                podIdentification: Math.random() > 0.5 ? pods[Math.floor(Math.random() * pods.length)] : null,
                behavior: behaviors[Math.floor(Math.random() * behaviors.length)],
                confidence: 0.6 + (Math.random() * 0.3),
                source: 'Orca Behavior Institute (BlueSky Mock)',
                sourceType: 'social_media_report',
                originalText: `Mock whale sighting report for ${location.name}`,
                platform: 'BlueSky'
            });
        }
        
        return mockSightings;
    }

    /**
     * Load existing sightings
     */
    loadExistingSightings() {
        try {
            if (fs.existsSync(this.dataFile)) {
                const data = JSON.parse(fs.readFileSync(this.dataFile, 'utf8'));
                return data.blueskySightings || [];
            }
        } catch (error) {
            console.error('Error loading existing sightings:', error);
        }
        
        return [];
    }
}

module.exports = BlueSkyImporter; 