/**
 * Scheduled Data Importer
 * Orchestrates data imports from multiple sources several times per day
 * Combines Orcasound hydrophone data and BlueSky social media reports
 */

const fs = require('fs');
const path = require('path');
const OrcasoundImporter = require('./orcasound-importer');
const BlueSkyImporter = require('./bluesky-importer');
const AI4OrcasImporter = require('./ai4orcas-importer');
const FirestoreSync = require('../firestore-sync');

class ScheduledImporter {
    constructor() {
        this.orcasoundImporter = new OrcasoundImporter();
        this.blueSkyImporter = new BlueSkyImporter();
        this.ai4orcasImporter = new AI4OrcasImporter();
        this.firestoreSync = new FirestoreSync();
        this.combinedDataFile = path.join(__dirname, '../data/combined_whale_sightings.json');
        this.scheduleFile = path.join(__dirname, '../data/import_schedule.json');
        
        // Import schedule: 4 times per day (every 6 hours)
        this.importIntervals = [
            { hour: 6, minute: 0 },   // 6:00 AM
            { hour: 12, minute: 0 },  // 12:00 PM  
            { hour: 18, minute: 0 },  // 6:00 PM
            { hour: 0, minute: 0 }    // 12:00 AM
        ];
        
        this.isRunning = false;
        this.scheduledTimeouts = [];
        
        // Ensure data directory exists
        const dataDir = path.dirname(this.combinedDataFile);
        if (!fs.existsSync(dataDir)) {
            fs.mkdirSync(dataDir, { recursive: true });
        }
    }

    /**
     * Start the scheduled import system
     */
    start() {
        if (this.isRunning) {
            console.log('⏰ Scheduled importer already running');
            return;
        }
        
        this.isRunning = true;
        console.log('🚀 Starting scheduled whale data importer...');
        
        // Run initial import
        this.runImport();
        
        // Schedule recurring imports
        this.scheduleNextImports();
        
        console.log('✅ Scheduled importer started - importing 4x daily');
        this.logNextImportTimes();
    }

    /**
     * Stop the scheduled import system
     */
    stop() {
        this.isRunning = false;
        
        // Clear all scheduled timeouts
        this.scheduledTimeouts.forEach(timeout => clearTimeout(timeout));
        this.scheduledTimeouts = [];
        
        console.log('⏹️ Scheduled importer stopped');
    }

    /**
     * Schedule the next set of imports
     */
    scheduleNextImports() {
        // Clear existing schedules
        this.scheduledTimeouts.forEach(timeout => clearTimeout(timeout));
        this.scheduledTimeouts = [];
        
        const now = new Date();
        
        this.importIntervals.forEach(interval => {
            const nextImport = new Date();
            nextImport.setHours(interval.hour, interval.minute, 0, 0);
            
            // If time has passed today, schedule for tomorrow
            if (nextImport <= now) {
                nextImport.setDate(nextImport.getDate() + 1);
            }
            
            const timeUntilImport = nextImport.getTime() - now.getTime();
            
            const timeout = setTimeout(() => {
                this.runImport();
                // Reschedule for the next day
                this.scheduleNextImports();
            }, timeUntilImport);
            
            this.scheduledTimeouts.push(timeout);
        });
        
        this.saveScheduleInfo();
    }

    /**
     * Run a complete import cycle
     */
    async runImport() {
        const startTime = Date.now();
        console.log(`\n🌊 Starting whale data import cycle at ${new Date().toLocaleString()}`);
        
        const importResults = {
            timestamp: new Date().toISOString(),
            orcasound: { status: 'pending', count: 0, error: null },
            bluesky: { status: 'pending', count: 0, error: null },
            combined: { status: 'pending', totalCount: 0 }
        };
        
        try {
            // Import from Orcasound (acoustic detections)
            console.log('🎵 Importing Orcasound hydrophone data...');
            try {
                const orcasoundData = await this.orcasoundImporter.importReports();
                importResults.orcasound = {
                    status: 'success',
                    count: orcasoundData.length,
                    error: null
                };
                console.log(`✅ Orcasound: ${orcasoundData.length} detections imported`);
            } catch (error) {
                importResults.orcasound = {
                    status: 'error',
                    count: 0,
                    error: error.message
                };
                console.error('❌ Orcasound import failed:', error.message);
            }
            
            // Import from BlueSky (social media reports)  
            console.log('🐦 Importing BlueSky social media reports...');
            try {
                const blueSkyData = await this.blueSkyImporter.importSightings();
                importResults.bluesky = {
                    status: 'success',
                    count: blueSkyData.length,
                    error: null
                };
                console.log(`✅ BlueSky: ${blueSkyData.length} sightings imported`);
            } catch (error) {
                importResults.bluesky = {
                    status: 'error',
                    count: 0,
                    error: error.message
                };
                console.error('❌ BlueSky import failed:', error.message);
            }
            
            // Combine all data sources
            const combinedData = await this.combineAllSources();
            importResults.combined = {
                status: 'success',
                totalCount: combinedData.allSightings.length
            };
            
            // Sync to Firestore for map configuration access
            console.log('🔥 Syncing data to Firestore...');
            try {
                const syncResult = await this.firestoreSync.syncSightingsData(combinedData.allSightings);
                importResults.firestore = {
                    status: 'success',
                    synced: syncResult.synced,
                    mode: syncResult.mode
                };
                console.log(`✅ Firestore sync: ${syncResult.synced} records (${syncResult.mode} mode)`);
            } catch (error) {
                importResults.firestore = {
                    status: 'error',
                    error: error.message
                };
                console.error('❌ Firestore sync failed:', error.message);
            }
            
            // Sync import status to Firestore
            try {
                await this.firestoreSync.syncImportStatus(importResults);
            } catch (error) {
                console.error('❌ Failed to sync import status to Firestore:', error.message);
            }
            
            // Log summary
            const duration = Date.now() - startTime;
            console.log(`\n📊 Import cycle completed in ${duration}ms:`);
            console.log(`   • Orcasound: ${importResults.orcasound.count} detections`);
            console.log(`   • BlueSky: ${importResults.bluesky.count} sightings`);
            console.log(`   • Combined total: ${importResults.combined.totalCount} records`);
            console.log(`   • Firestore: ${importResults.firestore?.synced || 0} synced (${importResults.firestore?.mode || 'error'})`);
            
        } catch (error) {
            console.error('❌ Import cycle failed:', error);
            importResults.combined.status = 'error';
        }
        
        // Save import results
        await this.saveImportResults(importResults);
        
        // Emit event for other components
        this.emitImportComplete(importResults);
    }

    /**
     * Combine data from all sources into unified format
     */
    async combineAllSources() {
        const allSightings = [];
        
        // Load Orcasound data
        try {
            const orcasoundData = this.orcasoundImporter.loadExistingReports();
            allSightings.push(...orcasoundData);
        } catch (error) {
            console.warn('Could not load Orcasound data:', error.message);
        }
        
        // Load BlueSky data
        try {
            const blueSkyData = this.blueSkyImporter.loadExistingSightings();
            allSightings.push(...blueSkyData);
        } catch (error) {
            console.warn('Could not load BlueSky data:', error.message);
        }
        
        // Note: Sample/fake data has been removed to use only real data sources
        console.log('Using only real data sources: Orcasound and BlueSky');
        
        // Remove duplicates and sort by timestamp
        const uniqueSightings = this.removeDuplicates(allSightings);
        const sortedSightings = uniqueSightings.sort((a, b) => 
            new Date(b.timestamp) - new Date(a.timestamp)
        );
        
        return {
            allSightings: sortedSightings,
            sources: {
                orcasound: this.orcasoundImporter.getStatus(),
                blueSky: this.blueSkyImporter.getStatus()
            },
            lastUpdated: new Date().toISOString()
        };
    }

    /**
     * Remove duplicate sightings based on timestamp and location
     */
    removeDuplicates(sightings) {
        const seen = new Set();
        return sightings.filter(sighting => {
            // Create a key based on timestamp (within 1 hour) and location
            const timestamp = new Date(sighting.timestamp);
            const hourKey = `${timestamp.getFullYear()}-${timestamp.getMonth()}-${timestamp.getDate()}-${timestamp.getHours()}`;
            const locationKey = sighting.location || 'unknown';
            const key = `${hourKey}_${locationKey}`;
            
            if (seen.has(key)) {
                return false; // Duplicate
            }
            
            seen.add(key);
            return true;
        });
    }

    /**
     * Get breakdown of sightings by source
     */
    getSourceBreakdown(sightings) {
        const breakdown = {};
        
        sightings.forEach(sighting => {
            const source = sighting.source || 'Unknown';
            breakdown[source] = (breakdown[source] || 0) + 1;
        });
        
        return breakdown;
    }

    /**
     * Save import results for monitoring
     */
    async saveImportResults(results) {
        const resultsFile = path.join(__dirname, '../data/import_results.json');
        
        let allResults = [];
        
        // Load existing results
        try {
            if (fs.existsSync(resultsFile)) {
                allResults = JSON.parse(fs.readFileSync(resultsFile, 'utf8'));
            }
        } catch (error) {
            console.warn('Could not load existing results:', error.message);
        }
        
        // Add new result
        allResults.unshift(results); // Add to beginning
        
        // Keep only last 50 results
        allResults = allResults.slice(0, 50);
        
        fs.writeFileSync(resultsFile, JSON.stringify(allResults, null, 2));
    }

    /**
     * Save schedule information
     */
    saveScheduleInfo() {
        const scheduleInfo = {
            status: this.isRunning ? 'running' : 'stopped',
            lastUpdated: new Date().toISOString(),
            nextImports: this.importIntervals.map(interval => {
                const next = new Date();
                next.setHours(interval.hour, interval.minute, 0, 0);
                if (next <= new Date()) {
                    next.setDate(next.getDate() + 1);
                }
                return {
                    time: `${interval.hour.toString().padStart(2, '0')}:${interval.minute.toString().padStart(2, '0')}`,
                    next: next.toISOString()
                };
            })
        };
        
        fs.writeFileSync(this.scheduleFile, JSON.stringify(scheduleInfo, null, 2));
    }

    /**
     * Log next import times
     */
    logNextImportTimes() {
        console.log('\n📅 Next scheduled imports:');
        this.importIntervals.forEach(interval => {
            const next = new Date();
            next.setHours(interval.hour, interval.minute, 0, 0);
            if (next <= new Date()) {
                next.setDate(next.getDate() + 1);
            }
            console.log(`   • ${interval.hour.toString().padStart(2, '0')}:${interval.minute.toString().padStart(2, '0')} - ${next.toLocaleDateString()} ${next.toLocaleTimeString()}`);
        });
    }

    /**
     * Emit import complete event
     */
    emitImportComplete(results) {
        // This would emit an event for other systems to listen to
        // For now, just log the completion
        console.log(`📡 Import complete event emitted with ${results.combined.totalCount} total sightings`);
    }

    /**
     * Get combined data for API consumption
     */
    getCombinedData() {
        try {
            if (fs.existsSync(this.combinedDataFile)) {
                return JSON.parse(fs.readFileSync(this.combinedDataFile, 'utf8'));
            }
        } catch (error) {
            console.error('Error loading combined data:', error);
        }
        
        return { allSightings: [], totalSightings: 0 };
    }

    /**
     * Force immediate import (for testing/manual trigger)
     */
    async forceImport() {
        console.log('🔧 Manual import triggered');
        await this.runImport();
    }

    /**
     * Get import status and statistics
     */
    getStatus() {
        const scheduleInfo = this.loadScheduleInfo();
        const lastResults = this.getLastImportResults();
        
        return {
            isRunning: this.isRunning,
            schedule: scheduleInfo,
            lastImport: lastResults,
            dataFiles: {
                combined: fs.existsSync(this.combinedDataFile),
                orcasound: fs.existsSync(this.orcasoundImporter.dataFile),
                bluesky: fs.existsSync(this.blueSkyImporter.dataFile)
            }
        };
    }

    /**
     * Load schedule information
     */
    loadScheduleInfo() {
        try {
            if (fs.existsSync(this.scheduleFile)) {
                return JSON.parse(fs.readFileSync(this.scheduleFile, 'utf8'));
            }
        } catch (error) {
            console.error('Error loading schedule info:', error);
        }
        
        return null;
    }

    /**
     * Get last import results
     */
    getLastImportResults() {
        try {
            const resultsFile = path.join(__dirname, '../data/import_results.json');
            if (fs.existsSync(resultsFile)) {
                const results = JSON.parse(fs.readFileSync(resultsFile, 'utf8'));
                return results[0] || null; // Most recent result
            }
        } catch (error) {
            console.error('Error loading import results:', error);
        }
        
        return null;
    }
}

module.exports = ScheduledImporter; 