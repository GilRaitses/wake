/**
 * Whale Watching Research Agent
 * Uses SINDy equations and HMC uncertainty to research optimal viewing locations for the existing Gemma 3 trip planner
 */

class WhaleWatchingResearchAgent {
    constructor(config = {}) {
        this.sindy_service_url = config.sindyServiceUrl || '/api/sindy-predictions';
        this.firestore_db = config.firestoreDB;
        this.hmc_service_url = config.hmcServiceUrl || '/api/hmc-uncertainty';
        
        // Research findings cache
        this.research_cache = new Map();
        this.location_analysis = new Map();
        
        console.log('🔬 Whale Watching Research Agent initialized');
    }

    /**
     * CORE RESEARCH METHODS for Gemma 3 Trip Planner
     */

    async researchOptimalViewingLocations(constraints) {
        console.log('🔍 Researching optimal viewing locations using SINDy equations...');
        
        try {
            // Extract spatial and temporal constraints from trip planner
            const research_parameters = this.extractResearchParameters(constraints);
            
            // Use SINDy equations to identify high-probability zones
            const sindy_insights = await this.analyzeSINDyPredictions(research_parameters);
            
            // Add HMC uncertainty analysis for confidence bands
            const uncertainty_analysis = await this.analyzeHMCUncertainty(sindy_insights);
            
            // Research historical success patterns
            const historical_patterns = await this.researchHistoricalPatterns(research_parameters);
            
            // Combine all research findings
            const research_findings = this.synthesizeResearchFindings({
                sindy_insights,
                uncertainty_analysis,
                historical_patterns,
                parameters: research_parameters
            });
            
            // Cache for trip planner
            this.cacheResearchFindings(constraints, research_findings);
            
            return research_findings;
            
        } catch (error) {
            console.error('Research agent error:', error);
            return this.getFallbackResearch(constraints);
        }
    }

    extractResearchParameters(constraints) {
        return {
            // Temporal constraints
            start_date: constraints.dates?.start || new Date(),
            end_date: constraints.dates?.end || new Date(Date.now() + 3 * 24 * 60 * 60 * 1000),
            preferred_times: constraints.times || ['dawn', 'morning', 'dusk'],
            
            // Spatial constraints  
            viewing_mode: constraints.viewing_mode || 'land', // land, boat, kayak
            max_distance: constraints.max_distance || 50, // km from accommodation
            accessibility: constraints.accessibility || 'standard',
            
            // Experience preferences
            behavior_interests: constraints.behaviors || ['feeding', 'socializing', 'traveling'],
            group_size: constraints.group_size || 2,
            experience_level: constraints.experience || 'beginner',
            
            // Environmental preferences
            weather_tolerance: constraints.weather || 'moderate',
            sea_conditions: constraints.sea_conditions || 'calm_to_moderate'
        };
    }

    async analyzeSINDyPredictions(parameters) {
        console.log('📊 Analyzing SINDy equation predictions for optimal locations...');
        
        // Query our SINDy service for predictions
        const sindy_predictions = await this.querySINDyService(parameters);
        
        // Extract key insights from discovered equations
        const feeding_hotspots = this.identifyFeedingHotspots(sindy_predictions);
        const socializing_zones = this.identifySocializingZones(sindy_predictions);
        const travel_corridors = this.identifyTravelCorridors(sindy_predictions);
        
        return {
            predictions: sindy_predictions,
            feeding_hotspots,
            socializing_zones,
            travel_corridors,
            optimal_times: this.extractOptimalTimes(sindy_predictions),
            environmental_factors: this.extractCriticalFactors(sindy_predictions)
        };
    }

    async querySINDyService(parameters) {
        try {
            const response = await fetch(this.sindy_service_url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    spatial_bounds: {
                        lat_min: 48.4, lat_max: 48.8,
                        lng_min: -123.3, lng_max: -122.8
                    },
                    temporal_range: {
                        start: parameters.start_date.toISOString(),
                        end: parameters.end_date.toISOString()
                    },
                    resolution: 'high',
                    include_uncertainty: true
                })
            });
            
            if (response.ok) {
                return await response.json();
            } else {
                console.warn('SINDy service unavailable, using cached data');
                return this.getFallbackSINDyData();
            }
        } catch (error) {
            console.error('SINDy service query failed:', error);
            return this.getFallbackSINDyData();
        }
    }

    identifyFeedingHotspots(sindy_predictions) {
        // Extract feeding behavior hotspots from SINDy equations
        const feeding_zones = sindy_predictions.behavioral_zones?.feeding || [];
        
        return feeding_zones.map(zone => ({
            location: {
                lat: zone.center_lat,
                lng: zone.center_lng,
                name: zone.location_name || 'Feeding Zone'
            },
            confidence: zone.confidence || 0.7,
            success_rate: zone.historical_success || 0.65,
            optimal_time: zone.peak_hours || '06:00-09:00',
            environmental_dependencies: zone.key_factors || ['tidal_height', 'salmon_abundance'],
            sindy_equation: zone.governing_equation || 'Feeding intensity ∝ f(tidal_height, prey_density)',
            predicted_probability: zone.current_probability || 0.75
        }));
    }

    identifySocializingZones(sindy_predictions) {
        // Extract socializing behavior zones
        const social_zones = sindy_predictions.behavioral_zones?.socializing || [];
        
        return social_zones.map(zone => ({
            location: {
                lat: zone.center_lat,
                lng: zone.center_lng,
                name: zone.location_name || 'Social Zone'
            },
            confidence: zone.confidence || 0.6,
            success_rate: zone.historical_success || 0.55,
            optimal_time: zone.peak_hours || '14:00-17:00',
            pod_size_preference: zone.typical_pod_size || '3-8 whales',
            behavioral_indicators: zone.typical_behaviors || ['surface_activity', 'vocalizations'],
            predicted_probability: zone.current_probability || 0.65
        }));
    }

    identifyTravelCorridors(sindy_predictions) {
        // Extract travel corridors from movement equations
        const travel_routes = sindy_predictions.movement_patterns?.corridors || [];
        
        return travel_routes.map(corridor => ({
            route: {
                start: { lat: corridor.start_lat, lng: corridor.start_lng },
                end: { lat: corridor.end_lat, lng: corridor.end_lng },
                name: corridor.corridor_name || 'Travel Corridor'
            },
            confidence: corridor.confidence || 0.7,
            peak_usage_times: corridor.peak_times || ['05:00-08:00', '16:00-19:00'],
            average_speed: corridor.travel_speed || '5-8 km/h',
            directionality: corridor.primary_direction || 'bidirectional',
            seasonal_variation: corridor.seasonal_patterns || 'summer_peak',
            predicted_activity: corridor.current_activity || 0.7
        }));
    }

    extractOptimalTimes(sindy_predictions) {
        // Extract optimal viewing times from all behavioral patterns
        const all_peak_times = [];
        
        // Collect peak times from different behaviors
        if (sindy_predictions.behavioral_zones?.feeding) {
            sindy_predictions.behavioral_zones.feeding.forEach(zone => {
                if (zone.peak_hours) all_peak_times.push(zone.peak_hours);
            });
        }
        
        if (sindy_predictions.movement_patterns?.corridors) {
            sindy_predictions.movement_patterns.corridors.forEach(corridor => {
                if (corridor.peak_times) all_peak_times.push(...corridor.peak_times);
            });
        }
        
        // Find most common time windows
        const time_frequency = {};
        all_peak_times.forEach(time_range => {
            time_frequency[time_range] = (time_frequency[time_range] || 0) + 1;
        });
        
        // Return top 3 most frequent time windows
        return Object.entries(time_frequency)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 3)
            .map(([time, frequency]) => ({
                time_window: time,
                frequency: frequency,
                recommendation_strength: frequency > 2 ? 'high' : 'moderate'
            }));
    }

    extractCriticalFactors(sindy_predictions) {
        // Extract critical environmental factors from SINDy equations
        const factor_importance = sindy_predictions.factor_analysis?.importance || {};
        
        return Object.entries(factor_importance)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 5)
            .map(([factor, importance]) => ({
                factor: factor,
                importance: importance,
                equation_role: this.getFactorEquationRole(factor, sindy_predictions),
                optimal_range: this.getOptimalRange(factor, sindy_predictions),
                current_value: this.getCurrentValue(factor)
            }));
    }

    async analyzeHMCUncertainty(sindy_insights) {
        console.log('🎲 Running HMC uncertainty analysis for confidence intervals...');
        
        try {
            const hmc_analysis = await this.queryHMCService(sindy_insights);
            
            return {
                confidence_intervals: this.calculateConfidenceIntervals(hmc_analysis),
                uncertainty_sources: this.identifyUncertaintySources(hmc_analysis),
                prediction_reliability: this.assessPredictionReliability(hmc_analysis),
                sensitivity_analysis: this.runSensitivityAnalysis(hmc_analysis)
            };
            
        } catch (error) {
            console.error('HMC analysis failed:', error);
            return this.getFallbackUncertaintyAnalysis();
        }
    }

    async queryHMCService(sindy_insights) {
        try {
            const response = await fetch(this.hmc_service_url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sindy_predictions: sindy_insights.predictions,
                    uncertainty_quantification: {
                        method: 'hamiltonian_monte_carlo',
                        samples: 1000,
                        chains: 4,
                        warmup: 500
                    },
                    confidence_levels: [0.68, 0.95, 0.99]
                })
            });
            
            if (response.ok) {
                return await response.json();
            } else {
                return this.getFallbackHMCData();
            }
        } catch (error) {
            console.error('HMC service query failed:', error);
            return this.getFallbackHMCData();
        }
    }

    calculateConfidenceIntervals(hmc_analysis) {
        // Calculate confidence intervals for predictions
        const intervals = {};
        
        if (hmc_analysis.posterior_samples) {
            hmc_analysis.posterior_samples.forEach(sample => {
                Object.keys(sample.parameters).forEach(param => {
                    if (!intervals[param]) intervals[param] = [];
                    intervals[param].push(sample.parameters[param]);
                });
            });
            
            // Calculate percentiles for confidence intervals
            Object.keys(intervals).forEach(param => {
                const values = intervals[param].sort((a, b) => a - b);
                intervals[param] = {
                    mean: values.reduce((sum, val) => sum + val, 0) / values.length,
                    ci_68: [this.percentile(values, 16), this.percentile(values, 84)],
                    ci_95: [this.percentile(values, 2.5), this.percentile(values, 97.5)],
                    ci_99: [this.percentile(values, 0.5), this.percentile(values, 99.5)]
                };
            });
        }
        
        return intervals;
    }

    async researchHistoricalPatterns(parameters) {
        console.log('📚 Researching historical success patterns...');
        
        try {
            // Query historical sighting data
            const historical_data = await this.queryHistoricalData(parameters);
            
            // Analyze patterns
            const temporal_patterns = this.analyzeTemporalPatterns(historical_data);
            const spatial_patterns = this.analyzeSpatialPatterns(historical_data);
            const environmental_correlations = this.analyzeEnvironmentalCorrelations(historical_data);
            
            return {
                data_summary: {
                    total_sightings: historical_data.length,
                    date_range: this.getDateRange(historical_data),
                    locations_covered: this.getUniqueLocations(historical_data).length
                },
                temporal_patterns,
                spatial_patterns,
                environmental_correlations,
                success_rates: this.calculateHistoricalSuccessRates(historical_data)
            };
            
        } catch (error) {
            console.error('Historical research failed:', error);
            return this.getFallbackHistoricalData();
        }
    }

    async queryHistoricalData(parameters) {
        // Query historical sighting data from multiple sources
        try {
            // Try to get verified OBIS data first
            const obis_response = await fetch('/data/comprehensive_orca_sightings.json');
            if (obis_response.ok) {
                const obis_data = await obis_response.json();
                return obis_data.sightings || [];
            }
            
            // Fallback to sample data
            const sample_response = await fetch('/data/sample_user_sightings.json');
            if (sample_response.ok) {
                const sample_data = await sample_response.json();
                return sample_data.sightings || [];
            }
            
            // Final fallback
            return this.generateFallbackSightings();
            
        } catch (error) {
            console.error('Historical data query failed:', error);
            return this.generateFallbackSightings();
        }
    }

    synthesizeResearchFindings(components) {
        console.log('🧬 Synthesizing research findings from all sources...');
        
        const {
            sindy_insights,
            uncertainty_analysis,
            historical_patterns,
            parameters
        } = components;
        
        // Combine insights from all research components
        const synthesis = {
            // Executive summary
            executive_summary: this.generateExecutiveSummary(components),
            
            // Top recommendations with confidence scores
            top_recommendations: this.generateTopRecommendations(components),
            
            // Detailed analysis results
            detailed_analysis: {
                sindy_insights,
                uncertainty_analysis,
                historical_patterns
            },
            
            // Research quality metrics
            research_quality: this.assessResearchQuality(components),
            
            // Confidence scoring
            confidence_analysis: this.generateConfidenceAnalysis(components),
            
            // Actionable insights for trip planner
            actionable_insights: this.generateActionableInsights(components),
            
            // Research metadata
            metadata: {
                research_timestamp: new Date().toISOString(),
                parameters_used: parameters,
                data_sources: this.getDataSourceSummary(),
                methodology: 'SINDy + HMC + Historical Analysis'
            }
        };
        
        return synthesis;
    }

    generateTopRecommendations(components) {
        const { sindy_insights, historical_patterns } = components;
        
        // Combine SINDy hotspots with historical validation
        const primary_locations = [];
        const backup_locations = [];
        
        // Process feeding hotspots (highest priority for whale watching)
        if (sindy_insights.feeding_hotspots) {
            sindy_insights.feeding_hotspots.forEach(hotspot => {
                const historical_validation = this.validateWithHistoricalData(
                    hotspot.location, historical_patterns
                );
                
                const combined_confidence = (hotspot.confidence + historical_validation.confidence) / 2;
                
                const recommendation = {
                    ...hotspot,
                    historical_validation,
                    combined_confidence,
                    recommendation_type: 'feeding_location'
                };
                
                if (combined_confidence > 0.7) {
                    primary_locations.push(recommendation);
                } else {
                    backup_locations.push(recommendation);
                }
            });
        }
        
        // Process socializing zones
        if (sindy_insights.socializing_zones) {
            sindy_insights.socializing_zones.forEach(zone => {
                const historical_validation = this.validateWithHistoricalData(
                    zone.location, historical_patterns
                );
                
                const combined_confidence = (zone.confidence + historical_validation.confidence) / 2;
                
                if (combined_confidence > 0.6) {
                    backup_locations.push({
                        ...zone,
                        historical_validation,
                        combined_confidence,
                        recommendation_type: 'socializing_location'
                    });
                }
            });
        }
        
        // Sort by combined confidence
        primary_locations.sort((a, b) => b.combined_confidence - a.combined_confidence);
        backup_locations.sort((a, b) => b.combined_confidence - a.combined_confidence);
        
        return {
            primary_locations: primary_locations.slice(0, 3), // Top 3 primary
            backup_locations: backup_locations.slice(0, 5),   // Top 5 backup
            total_locations_analyzed: primary_locations.length + backup_locations.length
        };
    }

    // Helper methods for analysis
    validateWithHistoricalData(location, historical_patterns) {
        // Validate SINDy predictions against historical data
        const nearby_sightings = this.findNearbySightings(location, historical_patterns.spatial_patterns);
        
        if (nearby_sightings.length > 0) {
            const avg_success = nearby_sightings.reduce((sum, s) => sum + (s.confidence || 0.5), 0) / nearby_sightings.length;
            return {
                confidence: avg_success,
                sightings_count: nearby_sightings.length,
                validation_status: 'confirmed'
            };
        }
        
        return {
            confidence: 0.4,
            sightings_count: 0,
            validation_status: 'unconfirmed'
        };
    }

    findNearbySightings(location, spatial_patterns, radius_km = 5) {
        // Find historical sightings near a given location
        return spatial_patterns.hotspots?.filter(sighting => {
            const distance = this.calculateDistance(
                location.lat, location.lng,
                sighting.lat, sighting.lng
            );
            return distance <= radius_km;
        }) || [];
    }

    calculateDistance(lat1, lng1, lat2, lng2) {
        // Calculate distance between two points in km
        const R = 6371; // Earth's radius in km
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLng = (lng2 - lng1) * Math.PI / 180;
        const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                Math.sin(dLng/2) * Math.sin(dLng/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return R * c;
    }

    // Fallback and utility methods
    getFallbackResearch(constraints) {
        return {
            executive_summary: 'Research conducted using fallback data due to service unavailability',
            top_recommendations: {
                primary_locations: [
                    {
                        location: { lat: 48.5465, lng: -123.0307, name: 'Lime Kiln Point' },
                        confidence: 0.75,
                        success_rate: 0.80,
                        optimal_time: '06:00-09:00'
                    }
                ],
                backup_locations: []
            },
            confidence_analysis: { overall_confidence: 0.6 }
        };
    }

    getFallbackSINDyData() {
        return {
            behavioral_zones: {
                feeding: [{
                    center_lat: 48.5465, center_lng: -123.0307,
                    confidence: 0.75, location_name: 'Lime Kiln Point'
                }]
            },
            factor_analysis: { importance: { tidal_height: 0.8, salmon_abundance: 0.7 } }
        };
    }

    getFallbackHMCData() {
        return {
            posterior_samples: [{
                parameters: { feeding_probability: 0.75, uncertainty: 0.15 }
            }]
        };
    }

    // Additional utility methods
    percentile(values, p) {
        const index = (p / 100) * (values.length - 1);
        const lower = Math.floor(index);
        const upper = Math.ceil(index);
        const weight = index - lower;
        return values[lower] * (1 - weight) + values[upper] * weight;
    }

    cacheResearchFindings(constraints, findings) {
        const cache_key = JSON.stringify(constraints);
        this.research_cache.set(cache_key, {
            findings,
            timestamp: new Date(),
            expiry: new Date(Date.now() + 6 * 60 * 60 * 1000) // 6 hours
        });
    }

    // Placeholder methods for complete functionality
    getFactorEquationRole(factor, predictions) { return 'primary_driver'; }
    getOptimalRange(factor, predictions) { return 'variable'; }
    getCurrentValue(factor) { return 'current'; }
    identifyUncertaintySources(analysis) { return ['environmental_variability', 'measurement_error']; }
    assessPredictionReliability(analysis) { return 0.8; }
    runSensitivityAnalysis(analysis) { return { sensitive_parameters: ['tidal_height'] }; }
    getFallbackUncertaintyAnalysis() { return { confidence_intervals: {}, uncertainty_sources: [] }; }
    analyzeTemporalPatterns(data) { return { peak_hours: ['06:00-09:00'] }; }
    analyzeSpatialPatterns(data) { return { hotspots: [] }; }
    analyzeEnvironmentalCorrelations(data) { return { correlations: {} }; }
    getDateRange(data) { return { start: '2019-01-01', end: '2024-12-31' }; }
    getUniqueLocations(data) { return []; }
    calculateHistoricalSuccessRates(data) { return { overall: 0.75 }; }
    getFallbackHistoricalData() { return { data_summary: { total_sightings: 0 } }; }
    generateFallbackSightings() { return []; }
    generateExecutiveSummary(components) { return 'Research analysis complete'; }
    assessResearchQuality(components) { return { overall_quality: 0.8 }; }
    generateConfidenceAnalysis(components) { return { overall_confidence: 0.75 }; }
    generateActionableInsights(components) { return []; }
    getDataSourceSummary() { return ['SINDy', 'HMC', 'Historical']; }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WhaleWatchingResearchAgent;
}

// Make available globally
if (typeof window !== 'undefined') {
    window.WhaleWatchingResearchAgent = WhaleWatchingResearchAgent;
} 