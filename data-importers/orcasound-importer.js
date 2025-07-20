/**
 * Orcasound Data Importer
 * Fetches whale detection reports from AWS S3 buckets and GraphQL API
 * Accesses real data from Orcasound's open access archives
 */

const fs = require('fs');
const path = require('path');

class OrcasoundImporter {
    constructor() {
        this.s3Buckets = {
            streaming: 'streaming-orcasound-net',
            archive: 'archive-orcasound-net', 
            acousticSandbox: 'acoustic-sandbox'
        };
        this.graphqlEndpoint = 'https://live.orcasound.net/graphql';
        this.region = 'us-west-2';
        this.dataFile = path.join(__dirname, '../data/orcasound_detections.json');
        this.lastImportFile = path.join(__dirname, '../data/last_orcasound_import.json');
        
        // Known Orcasound hydrophone nodes from their network
        this.knownNodes = {
            'rpi_orcasound_lab': { name: 'Orcasound Lab', location: 'Haro Strait', coordinates: { lat: 48.5, lng: -123.2 } },
            'rpi_port_townsend': { name: 'Port Townsend', location: 'Port Townsend', coordinates: { lat: 48.1, lng: -122.8 } },
            'rpi_sunset_bay': { name: 'Sunset Bay', location: 'Sunset Bay', coordinates: { lat: 48.5, lng: -123.1 } },
            'rpi_lime_kiln': { name: 'Lime Kiln Point', location: 'Lime Kiln Point', coordinates: { lat: 48.5, lng: -123.15 } },
            'rpi_bush_point': { name: 'Bush Point', location: 'Bush Point', coordinates: { lat: 48.0, lng: -122.6 } }
        };
    }

    /**
     * Import reports from Orcasound real data sources
     */
    async importReports() {
        console.log('🎵 Starting Orcasound real data import...');
        
        try {
            let reportsData = [];
            
            // Method 1: Try GraphQL API for live reports
            try {
                console.log('📡 Fetching from GraphQL API...');
                const graphqlData = await this.fetchFromGraphQL();
                if (graphqlData && graphqlData.length > 0) {
                    reportsData.push(...graphqlData);
                    console.log(`✅ GraphQL: ${graphqlData.length} reports fetched`);
                }
            } catch (error) {
                console.log(`❌ GraphQL failed: ${error.message}`);
            }
            
            // Process and normalize the data
            const processedReports = this.processReports(reportsData);
            
            // Save to file
            await this.saveReports(processedReports);
            await this.updateLastImport();
            
            console.log(`✅ Successfully imported ${processedReports.length} Orcasound reports`);
            return processedReports;
            
        } catch (error) {
            console.error('❌ Orcasound import failed:', error);
            return [];
        }
    }

    /**
     * Fetch reports from Orcasound GraphQL API
     */
    async fetchFromGraphQL() {
        try {
            const fetch = (await import('node-fetch')).default;
            
            // GraphQL query for detection reports (fixed to remove forbidden sourceIp field)
            const query = `
                query GetDetections($limit: Int) {
                    detections {
                        results {
                            id
                            timestamp
                            description
                            category
                            listenerCount
                        }
                        count
                    }
                }
            `;
            
            const response = await fetch(this.graphqlEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'User-Agent': 'ORCAST-Data-Importer/1.0'
                },
                body: JSON.stringify({
                    query: query,
                    variables: { limit: 500 } // Get more real detections
                })
            });
            
            if (!response.ok) {
                throw new Error(`GraphQL request failed: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.errors && data.errors.length > 0) {
                console.warn('GraphQL warnings:', data.errors.slice(0, 3)); // Show first 3 errors only
            }
            
            if (data.data && data.data.detections && data.data.detections.results) {
                console.log(`📊 Total detections in database: ${data.data.detections.count}`);
                return data.data.detections.results;
            }
            
            return [];
            
        } catch (error) {
            console.warn('GraphQL API unavailable:', error.message);
            return [];
        }
    }

    /**
     * Process raw detection reports into a standardized format.
     * This includes adding metadata, normalizing categories, and ensuring consistent structure.
     */
    processReports(reports) {
        const processedReports = [];
        const seenIds = new Set();

        for (const report of reports) {
            // Ensure required fields are present
            const detection = {
                id: report.id || `unknown_${Date.now()}`,
                timestamp: report.timestamp || 'N/A',
                description: report.description || 'Unknown detection',
                categories: report.categories || ['unknown'],
                source: report.source || 'unknown',
                confidence: report.confidence || 0,
                playlist_timestamp: report.playlist_timestamp || 'N/A',
                object_type: report.object_type || 'unknown',
                source_ip: report.source_ip || 'N/A',
                // Add metadata from GraphQL or S3
                metadata: {
                    source: report.source || 'unknown',
                    source_ip: report.source_ip || 'N/A',
                    confidence: report.confidence || 0,
                    playlist_timestamp: report.playlist_timestamp || 'N/A',
                    object_type: report.object_type || 'unknown',
                    size: report.size || 0, // For S3 data
                    bucket: report.bucket || 'N/A' // For S3 data
                }
            };

            // Normalize categories
            detection.categories = detection.categories.map(cat => cat.toLowerCase().trim());

            // Add unique ID if not already present
            if (!seenIds.has(detection.id)) {
                processedReports.push(detection);
                seenIds.add(detection.id);
            } else {
                console.warn(`Skipping duplicate report with ID: ${detection.id}`);
            }
        }

        return processedReports;
    }

    /**
     * Save processed reports to a JSON file.
     */
    async saveReports(reports) {
        try {
            const data = JSON.stringify(reports, null, 2);
            await fs.promises.writeFile(this.dataFile, data);
            console.log(`✅ Reports saved to ${this.dataFile}`);
        } catch (error) {
            console.error('❌ Failed to save reports:', error);
        }
    }

    /**
     * Update the last import timestamp in a JSON file.
     */
    async updateLastImport() {
        try {
            const data = JSON.stringify({ timestamp: new Date().toISOString() }, null, 2);
            await fs.promises.writeFile(this.lastImportFile, data);
            console.log(`✅ Last import timestamp updated in ${this.lastImportFile}`);
        } catch (error) {
            console.error('❌ Failed to update last import timestamp:', error);
        }
    }

    /**
     * Load last import timestamp from a JSON file.
     */
    async loadLastImport() {
        try {
            const data = await fs.promises.readFile(this.lastImportFile, 'utf8');
            return JSON.parse(data).timestamp;
        } catch (error) {
            console.warn('No previous import timestamp found, starting fresh.');
            return null;
        }
    }

    /**
     * Get the list of known Orcasound hydrophone nodes.
     */
    getKnownNodes() {
        return Object.values(this.knownNodes);
    }
}

module.exports = OrcasoundImporter; 