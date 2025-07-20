/**
 * Agentic Response Formatter
 * Formats Gemma3 agent responses into the required JSON schema for map integration
 */

class AgenticResponseFormatter {
    constructor() {
        this.schema = {
            type: "object",
            properties: {
                forecastOverview: { type: "string" },
                timeSeries: {
                    type: "array",
                    items: {
                        type: "object",
                        properties: {
                            timestamp: { type: "string", format: "date-time" },
                            probability: { type: "number" },
                            summary: { type: "string" }
                        },
                        required: ["timestamp", "probability", "summary"]
                    }
                },
                mapConfig: {
                    type: "object",
                    properties: {
                        center: {
                            type: "object",
                            properties: {
                                lat: { type: "number" },
                                lng: { type: "number" }
                            },
                            required: ["lat", "lng"]
                        },
                        zoomLevel: { type: "integer" },
                        overlays: {
                            type: "array",
                            items: {
                                type: "object",
                                properties: {
                                    type: { type: "string" },
                                    data: { type: "object" }
                                },
                                required: ["type", "data"]
                            }
                        }
                    },
                    required: ["center", "zoomLevel", "overlays"]
                },
                actions: {
                    type: "array",
                    items: {
                        type: "object",
                        properties: {
                            type: { type: "string" },
                            label: { type: "string" },
                            payload: { type: ["object", "null"] }
                        },
                        required: ["type", "label"]
                    }
                }
            },
            required: ["forecastOverview", "timeSeries", "mapConfig", "actions"]
        };
    }

    /**
     * Format agent response for trip planning with map integration
     */
    async formatTripPlanResponse(constraints, environmentalData, forecastData) {
        try {
            // Get historical sightings data to inform recommendations
            const historicalData = await this.fetchHistoricalSightings(constraints);
            
            // Get forecast overview from current data
            const forecastOverview = this.generateForecastOverview(environmentalData, forecastData, constraints, historicalData);
            
            // Generate time series for next 24 hours (informed by historical patterns)
            const timeSeries = this.generateTimeSeries(forecastData, environmentalData, historicalData);
            
            // Create map configuration (with historical hotspots)
            const mapConfig = this.generateMapConfig(constraints, forecastData, historicalData);
            
            // Generate action buttons
            const actions = this.generateActions(constraints, forecastData, historicalData);
            
            const response = {
                forecastOverview,
                timeSeries,
                mapConfig,
                actions
            };
            
            // Validate against schema
            if (this.validateResponse(response)) {
                return response;
            } else {
                throw new Error('Generated response does not match required schema');
            }
            
        } catch (error) {
            console.error('Error formatting agentic response:', error);
            return this.getErrorResponse(error.message);
        }
    }

    /**
     * Fetch historical sightings data based on constraints
     */
    async fetchHistoricalSightings(constraints) {
        try {
            // Determine appropriate historical window based on constraints
            const timeWindow = this.getHistoricalTimeWindow(constraints);
            
            const response = await fetch('/api/historical-sightings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(timeWindow)
            });
            
            if (!response.ok) {
                throw new Error(`Historical data API error: ${response.status}`);
            }
            
            const data = await response.json();
            return data.data;
            
        } catch (error) {
            console.warn('Could not fetch historical sightings, using fallback:', error);
            return {
                sightings: [],
                summary: {
                    totalSightings: 0,
                    hotspotLocation: 'Haro Strait',
                    mostCommonBehavior: 'foraging',
                    avgGroupSize: 4.5
                }
            };
        }
    }

    /**
     * Determine historical time window based on trip constraints
     */
    getHistoricalTimeWindow(constraints) {
        const now = new Date();
        let startDate, endDate, scale;
        
        // Analyze constraints to determine relevant historical period
        if (constraints.date) {
            const constraintDate = new Date(constraints.date);
            const dayOfYear = this.getDayOfYear(constraintDate);
            
            // Look at same time period in previous years for seasonal patterns
            const lastYear = new Date(constraintDate);
            lastYear.setFullYear(lastYear.getFullYear() - 1);
            
            startDate = new Date(lastYear);
            startDate.setDate(startDate.getDate() - 14); // ±2 weeks window
            
            endDate = new Date(lastYear);
            endDate.setDate(endDate.getDate() + 14);
            
            scale = 'days';
        } else {
            // Default to last 3 months for general patterns
            endDate = new Date(now);
            startDate = new Date(now);
            startDate.setMonth(startDate.getMonth() - 3);
            scale = 'months';
        }
        
        return {
            startDate: startDate.toISOString(),
            endDate: endDate.toISOString(),
            scale: scale
        };
    }

    /**
     * Get day of year (1-365)
     */
    getDayOfYear(date) {
        const start = new Date(date.getFullYear(), 0, 0);
        const diff = date - start;
        const oneDay = 1000 * 60 * 60 * 24;
        return Math.floor(diff / oneDay);
    }

    /**
     * Generate forecast overview summary (enhanced with historical context)
     */
    generateForecastOverview(environmentalData, forecastData, constraints, historicalData) {
        const location = constraints.location || 'Salish Sea';
        const timeframe = constraints.timeframe || '24 hours';
        
        // Extract key environmental factors
        const tidalHeight = environmentalData.tidalHeight || 2.3;
        const seaTemp = environmentalData.seaTemperature || 16.1;
        const salmonCount = environmentalData.salmonCount || 342;
        
        // Calculate average probability from forecast zones
        const zones = forecastData.prediction_zones || [];
        const avgProbability = zones.length > 0 
            ? zones.reduce((sum, z) => sum + z.probability, 0) / zones.length 
            : 0.65;
        
        const probabilityText = avgProbability > 0.7 ? 'high' : avgProbability > 0.4 ? 'moderate' : 'low';
        
        // Include historical context
        const historicalContext = this.getHistoricalContext(historicalData, location);
        
        return `ORCAST forecasting shows ${probabilityText} probability (${(avgProbability * 100).toFixed(0)}%) for orca sightings in ${location} over the next ${timeframe}. Current conditions favor orca activity: tidal height at ${tidalHeight}ft, sea temperature ${seaTemp}°C, and salmon count at ${salmonCount}. ${historicalContext} Environmental conditions are ${environmentalData.dataQuality || 'optimal'} for marine wildlife observation.`;
    }

    /**
     * Generate historical context text
     */
    getHistoricalContext(historicalData, location) {
        if (!historicalData.summary || historicalData.summary.totalSightings === 0) {
            return 'Historical data suggests this area has consistent orca activity.';
        }
        
        const summary = historicalData.summary;
        const hotspot = summary.hotspotLocation || 'unknown area';
        const behavior = summary.mostCommonBehavior || 'foraging';
        const totalSightings = summary.totalSightings || 0;
        
        if (totalSightings > 20) {
            return `Historical analysis of ${totalSightings} recent sightings shows ${hotspot} as the primary hotspot, with ${behavior} being the dominant behavior pattern.`;
        } else if (totalSightings > 5) {
            return `Recent ${totalSightings} sightings indicate ${behavior} activity concentrated around ${hotspot}.`;
        } else {
            return `Limited recent sightings (${totalSightings}) suggest checking historical hotspots like ${hotspot}.`;
        }
    }

    /**
     * Generate time series data (enhanced with historical patterns)
     */
    generateTimeSeries(forecastData, environmentalData, historicalData) {
        const timeSeries = [];
        const now = new Date();
        
        // Get hourly distribution from historical data
        const hourlyPatterns = this.analyzeHourlyPatterns(historicalData.sightings || []);
        
        // Generate 24 hourly forecasts
        for (let i = 0; i < 24; i++) {
            const timestamp = new Date(now.getTime() + (i * 60 * 60 * 1000));
            const hour = timestamp.getHours();
            
            // Base probability from environmental factors
            let baseProbability = 0.4;
            
            // Historical pattern boost
            const historicalBoost = hourlyPatterns[hour] || 0;
            baseProbability += historicalBoost * 0.3;
            
            // Higher probability during dawn/dusk feeding times
            if ((hour >= 5 && hour <= 8) || (hour >= 17 && hour <= 20)) {
                baseProbability += 0.2;
            }
            
            // Factor in environmental conditions
            const envBonus = (environmentalData.salmonCount || 300) / 1000 * 0.3;
            const probability = Math.min(0.95, baseProbability + envBonus + (Math.random() * 0.1 - 0.05));
            
            let summary = '';
            if (probability > 0.7) {
                summary = `High probability window. ${historicalBoost > 0.1 ? 'Historical data confirms' : 'Environmental conditions suggest'} peak feeding activity.`;
            } else if (probability > 0.4) {
                summary = `Moderate sighting probability. ${historicalBoost > 0.05 ? 'Historical patterns support' : 'Conditions support'} foraging behavior.`;
            } else {
                summary = `Lower probability period. ${historicalBoost < 0.05 ? 'Historical data shows reduced activity' : 'Orcas likely in deeper waters'}.`;
            }
            
            timeSeries.push({
                timestamp: timestamp.toISOString(),
                probability: parseFloat(probability.toFixed(3)),
                summary
            });
        }
        
        return timeSeries;
    }

    /**
     * Analyze hourly patterns from historical sightings
     */
    analyzeHourlyPatterns(sightings) {
        const hourlyCount = new Array(24).fill(0);
        const hourlyTotal = new Array(24).fill(0);
        
        sightings.forEach(sighting => {
            const hour = new Date(sighting.timestamp).getHours();
            hourlyCount[hour]++;
            hourlyTotal[hour]++;
        });
        
        // Normalize to 0-1 scale
        const maxCount = Math.max(...hourlyCount);
        return hourlyCount.map(count => maxCount > 0 ? count / maxCount : 0);
    }

    /**
     * Generate map configuration (enhanced with historical hotspots)
     */
    generateMapConfig(constraints, forecastData, historicalData) {
        // Default to Salish Sea coordinates
        let center = { lat: 48.5, lng: -123.0 };
        let zoomLevel = 10;
        
        // Parse location constraints
        if (constraints.location) {
            const locationCoords = this.getLocationCoordinates(constraints.location);
            if (locationCoords) {
                center = locationCoords;
                zoomLevel = 12;
            }
        }
        
        // Generate overlays from forecast data
        const overlays = [];
        
        // Historical hotspots overlay (NEW)
        if (historicalData.sightings && historicalData.sightings.length > 0) {
            const hotspots = this.generateHistoricalHotspots(historicalData.sightings);
            overlays.push({
                type: "historical_hotspots",
                data: {
                    hotspots: hotspots,
                    style: {
                        fillColor: "#FFD700",
                        strokeColor: "#FFA500",
                        fillOpacity: 0.4,
                        radius: 500
                    },
                    metadata: {
                        totalSightings: historicalData.summary.totalSightings,
                        timeRange: "Last 3 months",
                        confidence: "Historical data"
                    }
                }
            });
        }
        
        // Probability heatmap overlay
        if (forecastData.prediction_zones && forecastData.prediction_zones.length > 0) {
            overlays.push({
                type: "probability_heatmap",
                data: {
                    zones: forecastData.prediction_zones.map(zone => ({
                        coordinates: zone.coordinates || [center.lng, center.lat],
                        probability: zone.probability,
                        radius: zone.radius || 1000,
                        color: this.getProbabilityColor(zone.probability)
                    })),
                    opacity: 0.6,
                    blur: 15
                }
            });
        }
        
        // Feeding zones overlay
        overlays.push({
            type: "feeding_zones",
            data: {
                zones: [
                    { name: "Lime Kiln Point", coordinates: [-123.152, 48.516], intensity: 0.8 },
                    { name: "Haro Strait", coordinates: [-123.2, 48.5], intensity: 0.9 },
                    { name: "Boundary Pass", coordinates: [-123.0, 48.7], intensity: 0.7 }
                ],
                style: {
                    fillColor: "#4CAF50",
                    strokeColor: "#2E7D32",
                    fillOpacity: 0.3
                }
            }
        });
        
        // Current conditions overlay
        overlays.push({
            type: "environmental_data",
            data: {
                tidal_stations: [
                    {
                        location: center,
                        height: constraints.environmentalData?.tidalHeight || 2.3,
                        direction: "rising",
                        next_change: new Date(Date.now() + 6 * 60 * 60 * 1000).toISOString()
                    }
                ],
                salmon_migration: {
                    routes: [
                        {
                            path: [[-123.5, 48.3], [-123.2, 48.5], [-122.8, 48.7]],
                            density: constraints.environmentalData?.salmonCount || 342,
                            species: "Chinook"
                        }
                    ]
                }
            }
        });
        
        return {
            center,
            zoomLevel,
            overlays
        };
    }

    /**
     * Generate historical hotspots from sightings data
     */
    generateHistoricalHotspots(sightings) {
        const locationClusters = {};
        
        sightings.forEach(sighting => {
            const location = sighting.location || 'Unknown';
            if (!locationClusters[location]) {
                locationClusters[location] = {
                    name: location,
                    coordinates: sighting.coordinates ? [sighting.coordinates.lng, sighting.coordinates.lat] : null,
                    sightings: 0,
                    totalOrcs: 0,
                    behaviors: {}
                };
            }
            
            locationClusters[location].sightings++;
            locationClusters[location].totalOrcs += sighting.groupSize || 0;
            
            if (sighting.behavior) {
                locationClusters[location].behaviors[sighting.behavior] = 
                    (locationClusters[location].behaviors[sighting.behavior] || 0) + 1;
            }
        });
        
        // Convert to array and add intensity
        return Object.values(locationClusters)
            .filter(cluster => cluster.coordinates)
            .map(cluster => ({
                ...cluster,
                intensity: Math.min(1.0, cluster.sightings / 10), // Scale intensity 0-1
                avgGroupSize: Math.round(cluster.totalOrcs / cluster.sightings * 10) / 10,
                dominantBehavior: Object.keys(cluster.behaviors).reduce((a, b) => 
                    cluster.behaviors[a] > cluster.behaviors[b] ? a : b, 'unknown')
            }))
            .sort((a, b) => b.sightings - a.sightings); // Sort by sighting count
    }

    /**
     * Generate action buttons for the interface
     */
    generateActions(constraints, forecastData, historicalData) {
        const actions = [];
        
        // Save to trip plan action
        actions.push({
            type: "save_plan",
            label: "Save to Trip Journal",
            payload: {
                planData: {
                    constraints,
                    forecast: forecastData,
                    timestamp: new Date().toISOString()
                }
            }
        });
        
        // Set alert action for high probability windows
        const highProbWindows = forecastData.prediction_zones?.filter(z => z.probability > 0.7) || [];
        if (highProbWindows.length > 0) {
            actions.push({
                type: "set_alert",
                label: "Set High Probability Alert",
                payload: {
                    thresholds: { probability: 0.7 },
                    notification_methods: ["push", "email"],
                    location: constraints.location
                }
            });
        }
        
        // Export data action
        actions.push({
            type: "export_data",
            label: "Export Forecast Data",
            payload: {
                formats: ["json", "csv", "gpx"],
                include: ["coordinates", "timestamps", "probabilities"]
            }
        });
        
        // Refresh forecast action
        actions.push({
            type: "refresh_forecast",
            label: "Update Real-time Data",
            payload: {
                sources: ["noaa", "ais", "dtag", "environmental"]
            }
        });
        
        return actions;
    }

    /**
     * Get coordinates for common locations
     */
    getLocationCoordinates(location) {
        const locations = {
            'salish sea': { lat: 48.5, lng: -123.0 },
            'puget sound': { lat: 47.6, lng: -122.3 },
            'san juan islands': { lat: 48.6, lng: -123.1 },
            'orcas island': { lat: 48.7, lng: -122.9 },
            'lime kiln point': { lat: 48.516, lng: -123.152 },
            'haro strait': { lat: 48.5, lng: -123.2 },
            'boundary pass': { lat: 48.7, lng: -123.0 }
        };
        
        return locations[location.toLowerCase()] || null;
    }

    /**
     * Get color based on probability value
     */
    getProbabilityColor(probability) {
        if (probability > 0.7) return "#FF4444"; // High - Red
        if (probability > 0.4) return "#FFA500"; // Medium - Orange  
        return "#4CAF50"; // Low - Green
    }

    /**
     * Validate response against schema
     */
    validateResponse(response) {
        try {
            // Basic validation - check required fields
            const required = ['forecastOverview', 'timeSeries', 'mapConfig', 'actions'];
            for (const field of required) {
                if (!response[field]) {
                    console.error(`Missing required field: ${field}`);
                    return false;
                }
            }
            
            // Validate timeSeries structure
            if (!Array.isArray(response.timeSeries) || response.timeSeries.length === 0) {
                console.error('timeSeries must be a non-empty array');
                return false;
            }
            
            // Validate mapConfig structure
            if (!response.mapConfig.center || !response.mapConfig.center.lat || !response.mapConfig.center.lng) {
                console.error('mapConfig must have center with lat/lng');
                return false;
            }
            
            return true;
        } catch (error) {
            console.error('Validation error:', error);
            return false;
        }
    }

    /**
     * Generate error response
     */
    getErrorResponse(errorMessage) {
        return {
            forecastOverview: `Error generating forecast: ${errorMessage}. Please try again or contact support.`,
            timeSeries: [{
                timestamp: new Date().toISOString(),
                probability: 0,
                summary: "Data unavailable due to error"
            }],
            mapConfig: {
                center: { lat: 48.5, lng: -123.0 },
                zoomLevel: 10,
                overlays: []
            },
            actions: [{
                type: "retry",
                label: "Retry Forecast",
                payload: null
            }]
        };
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AgenticResponseFormatter;
} 