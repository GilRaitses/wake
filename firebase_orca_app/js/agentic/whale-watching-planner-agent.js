/**
 * Whale Watching Planner Agent
 * Creates sustainable viewing routes using SINDy research and HMC uncertainty data
 * Supports the existing Gemma 3 trip planning agent
 */

class WhaleWatchingPlannerAgent {
    constructor(config = {}) {
        this.research_agent = config.researchAgent || new WhaleWatchingResearchAgent(config);
        this.google_maps_api = config.googleMapsAPI;
        this.sustainability_weights = config.sustainabilityWeights || {
            environmental_impact: 0.3,
            wildlife_disturbance: 0.4,
            community_benefit: 0.2,
            educational_value: 0.1
        };
        
        // Route planning cache
        this.route_cache = new Map();
        this.optimization_cache = new Map();
        
        console.log('📋 Whale Watching Planner Agent initialized');
    }

    /**
     * CORE PLANNING METHODS for Gemma 3 Trip Planner
     */

    async planSustainableViewingRoutes(constraints, research_findings) {
        console.log('🗺️ Planning sustainable whale watching routes...');
        
        try {
            // Extract planning parameters from constraints
            const planning_params = this.extractPlanningParameters(constraints);
            
            // Create route options using research findings
            const route_options = await this.createRouteOptions(research_findings, planning_params);
            
            // Optimize routes for sustainability
            const optimized_routes = await this.optimizeForSustainability(route_options, planning_params);
            
            // Add timing and logistics
            const detailed_routes = await this.addRouteTiming(optimized_routes, research_findings);
            
            // Generate contingency plans
            const contingency_plans = await this.generateContingencyPlans(detailed_routes, research_findings);
            
            // Compile final route plan
            const final_plan = this.compileRoutePlan({
                primary_routes: detailed_routes,
                contingency_plans,
                research_evidence: research_findings,
                sustainability_metrics: this.calculateSustainabilityMetrics(detailed_routes)
            });
            
            // Cache for trip planner
            this.cacheRoutePlan(constraints, final_plan);
            
            return final_plan;
            
        } catch (error) {
            console.error('Planner agent error:', error);
            return this.getFallbackPlan(constraints);
        }
    }

    extractPlanningParameters(constraints) {
        return {
            // Trip structure
            trip_duration: constraints.duration || 3, // days
            daily_viewing_hours: constraints.viewing_hours || 6,
            travel_budget_hours: constraints.travel_time || 3, // max travel per day
            
            // Sustainability requirements
            max_daily_distance: constraints.max_distance || 100, // km
            group_size: constraints.group_size || 4,
            environmental_priority: constraints.sustainability || 'high',
            
            // Viewing preferences
            viewing_modes: constraints.viewing_modes || ['land', 'boat'],
            accessibility_needs: constraints.accessibility || [],
            photography_interests: constraints.photography || false,
            
            // Logistics
            accommodation_base: constraints.accommodation || { lat: 48.516, lng: -123.012 },
            transportation_mode: constraints.transport || 'car',
            meal_preferences: constraints.meals || 'local'
        };
    }

    async createRouteOptions(research_findings, params) {
        console.log('🛣️ Creating route options from research findings...');
        
        const primary_locations = research_findings.top_recommendations.primary_locations;
        const backup_locations = research_findings.top_recommendations.backup_locations;
        
        // Create different route strategies
        const route_strategies = [
            this.createHighProbabilityRoute(primary_locations, params),
            this.createDiverseBehaviorRoute(research_findings, params),
            this.createConservativeRoute(primary_locations, params),
            this.createAdventurousRoute([...primary_locations, ...backup_locations], params)
        ];
        
        // Filter routes based on parameters
        const viable_routes = route_strategies.filter(route => 
            this.validateRouteConstraints(route, params)
        );
        
        console.log(`Generated ${viable_routes.length} viable route options`);
        return viable_routes;
    }

    createHighProbabilityRoute(primary_locations, params) {
        // Focus on locations with highest success probability
        const sorted_locations = primary_locations
            .sort((a, b) => b.combined_confidence - a.combined_confidence)
            .slice(0, Math.min(5, primary_locations.length));
        
        return {
            strategy: 'high_probability',
            name: 'High Success Route',
            description: 'Focuses on locations with highest whale sighting probability',
            locations: sorted_locations,
            estimated_success_rate: this.calculateRouteSuccessRate(sorted_locations),
            total_distance: this.calculateRouteDistance(sorted_locations, params.accommodation_base),
            sustainability_score: this.calculateSustainabilityScore(sorted_locations, params)
        };
    }

    createDiverseBehaviorRoute(research_findings, params) {
        // Include diverse whale behaviors (feeding, socializing, traveling)
        const diverse_locations = [];
        
        // Add best feeding location
        const feeding_spots = research_findings.top_recommendations.primary_locations
            .filter(loc => loc.recommendation_type === 'feeding_location');
        if (feeding_spots.length > 0) {
            diverse_locations.push(feeding_spots[0]);
        }
        
        // Add best socializing location
        const social_spots = research_findings.top_recommendations.backup_locations
            .filter(loc => loc.recommendation_type === 'socializing_location');
        if (social_spots.length > 0) {
            diverse_locations.push(social_spots[0]);
        }
        
        // Add travel corridor observation points
        if (research_findings.detailed_analysis.sindy_insights.travel_corridors) {
            const travel_corridors = research_findings.detailed_analysis.sindy_insights.travel_corridors;
            if (travel_corridors.length > 0) {
                diverse_locations.push({
                    location: travel_corridors[0].route.start,
                    recommendation_type: 'travel_observation',
                    combined_confidence: travel_corridors[0].confidence,
                    optimal_time: travel_corridors[0].peak_usage_times[0]
                });
            }
        }
        
        return {
            strategy: 'diverse_behavior',
            name: 'Complete Behavior Experience',
            description: 'Covers feeding, socializing, and travel behaviors',
            locations: diverse_locations,
            estimated_success_rate: this.calculateRouteSuccessRate(diverse_locations),
            total_distance: this.calculateRouteDistance(diverse_locations, params.accommodation_base),
            educational_value: 'high'
        };
    }

    createConservativeRoute(primary_locations, params) {
        // Conservative route with short distances and high confidence
        const accessible_locations = primary_locations
            .filter(loc => this.isAccessible(loc, params.accessibility_needs))
            .sort((a, b) => {
                // Sort by confidence and proximity
                const confidence_diff = b.combined_confidence - a.combined_confidence;
                const distance_a = this.calculateDistance(loc.location, params.accommodation_base);
                const distance_b = this.calculateDistance(loc.location, params.accommodation_base);
                return confidence_diff !== 0 ? confidence_diff : distance_a - distance_b;
            })
            .slice(0, 3);
        
        return {
            strategy: 'conservative',
            name: 'Reliable Viewing Route',
            description: 'Short distances, high success probability, accessible locations',
            locations: accessible_locations,
            estimated_success_rate: this.calculateRouteSuccessRate(accessible_locations),
            total_distance: this.calculateRouteDistance(accessible_locations, params.accommodation_base),
            accessibility_rating: 'high'
        };
    }

    createAdventurousRoute(all_locations, params) {
        // More adventurous route including backup locations
        const adventurous_locations = all_locations
            .filter(loc => loc.combined_confidence > 0.5)
            .sort((a, b) => b.combined_confidence - a.combined_confidence)
            .slice(0, 7);
        
        return {
            strategy: 'adventurous',
            name: 'Explorer Route',
            description: 'Includes emerging hotspots and diverse locations',
            locations: adventurous_locations,
            estimated_success_rate: this.calculateRouteSuccessRate(adventurous_locations),
            total_distance: this.calculateRouteDistance(adventurous_locations, params.accommodation_base),
            exploration_factor: 'high'
        };
    }

    async optimizeForSustainability(route_options, params) {
        console.log('🌱 Optimizing routes for sustainability...');
        
        const optimized_routes = [];
        
        for (const route of route_options) {
            const optimization = await this.performSustainabilityOptimization(route, params);
            
            optimized_routes.push({
                ...route,
                optimization_applied: true,
                original_route: { ...route },
                sustainability_improvements: optimization.improvements,
                environmental_impact_reduction: optimization.impact_reduction,
                optimized_sequence: optimization.sequence,
                carbon_footprint: optimization.carbon_footprint
            });
        }
        
        // Sort by sustainability score
        optimized_routes.sort((a, b) => 
            b.sustainability_improvements.overall_score - 
            a.sustainability_improvements.overall_score
        );
        
        return optimized_routes;
    }

    async performSustainabilityOptimization(route, params) {
        // Multi-objective optimization for sustainability
        const improvements = {
            distance_optimization: this.optimizeDistance(route.locations),
            timing_optimization: this.optimizeForWildlifeWelfare(route.locations),
            impact_minimization: this.minimizeEnvironmentalImpact(route, params),
            community_integration: this.maximizeCommunityBenefit(route.locations),
            overall_score: 0
        };
        
        // Calculate overall sustainability score
        improvements.overall_score = (
            improvements.distance_optimization.score * this.sustainability_weights.environmental_impact +
            improvements.timing_optimization.score * this.sustainability_weights.wildlife_disturbance +
            improvements.impact_minimization.score * this.sustainability_weights.environmental_impact +
            improvements.community_integration.score * this.sustainability_weights.community_benefit
        );
        
        return {
            improvements,
            impact_reduction: this.calculateImpactReduction(improvements),
            sequence: this.optimizeSequence(route.locations),
            carbon_footprint: this.calculateCarbonFootprint(route, params)
        };
    }

    optimizeDistance(locations) {
        // Optimize travel distance using traveling salesman approximation
        const optimized_order = this.solveTSP(locations);
        const original_distance = this.calculateTotalDistance(locations);
        const optimized_distance = this.calculateTotalDistance(optimized_order);
        
        return {
            optimized_order,
            distance_saved: original_distance - optimized_distance,
            improvement_percentage: ((original_distance - optimized_distance) / original_distance) * 100,
            score: Math.min(1.0, (original_distance - optimized_distance) / original_distance * 2)
        };
    }

    optimizeForWildlifeWelfare(locations) {
        // Optimize timing to minimize wildlife disturbance
        const welfare_optimized_schedule = locations.map(location => {
            const optimal_time = location.optimal_time || '06:00-09:00';
            const disturbance_factor = this.calculateDisturbanceFactor(location);
            
            return {
                location,
                recommended_time: optimal_time,
                max_duration: this.calculateMaxViewingDuration(location),
                disturbance_minimization: disturbance_factor,
                wildlife_welfare_score: 1 - disturbance_factor
            };
        });
        
        const average_welfare_score = welfare_optimized_schedule
            .reduce((sum, item) => sum + item.wildlife_welfare_score, 0) / welfare_optimized_schedule.length;
        
        return {
            schedule: welfare_optimized_schedule,
            score: average_welfare_score,
            welfare_recommendations: this.generateWelfareRecommendations(welfare_optimized_schedule)
        };
    }

    async addRouteTiming(optimized_routes, research_findings) {
        console.log('⏰ Adding detailed timing to optimized routes...');
        
        const timed_routes = [];
        
        for (const route of optimized_routes) {
            const timing = await this.generateDetailedTiming(route, research_findings);
            
            timed_routes.push({
                ...route,
                detailed_timing: timing,
                daily_schedules: timing.daily_schedules,
                time_optimization: timing.optimization_summary,
                logistics: timing.logistics_plan
            });
        }
        
        return timed_routes;
    }

    async generateDetailedTiming(route, research_findings) {
        // Generate hour-by-hour timing for the route
        const daily_schedules = [];
        const locations_per_day = Math.ceil(route.locations.length / route.trip_duration || 3);
        
        for (let day = 1; day <= (route.trip_duration || 3); day++) {
            const day_locations = route.locations.slice(
                (day - 1) * locations_per_day,
                day * locations_per_day
            );
            
            const day_schedule = await this.createDaySchedule(day, day_locations, research_findings);
            daily_schedules.push(day_schedule);
        }
        
        return {
            daily_schedules,
            optimization_summary: this.summarizeTimeOptimization(daily_schedules),
            logistics_plan: this.createLogisticsPlan(daily_schedules)
        };
    }

    async createDaySchedule(day_number, locations, research_findings) {
        // Create detailed schedule for a single day
        const activities = [];
        let current_time = '06:00'; // Start early for best viewing
        
        for (const location of locations) {
            const viewing_duration = this.calculateOptimalViewingDuration(location);
            const travel_time = this.calculateTravelTime(activities.length > 0 ? 
                activities[activities.length - 1].location : null, location);
            
            // Add travel time
            if (travel_time > 0) {
                activities.push({
                    type: 'travel',
                    start_time: current_time,
                    end_time: this.addMinutes(current_time, travel_time),
                    duration_minutes: travel_time,
                    description: `Travel to ${location.location.name}`
                });
                current_time = this.addMinutes(current_time, travel_time);
            }
            
            // Add viewing activity
            activities.push({
                type: 'whale_viewing',
                location: location,
                start_time: current_time,
                end_time: this.addMinutes(current_time, viewing_duration),
                duration_minutes: viewing_duration,
                success_probability: location.combined_confidence,
                optimal_conditions: location.optimal_time,
                description: `Whale viewing at ${location.location.name}`
            });
            
            current_time = this.addMinutes(current_time, viewing_duration + 15); // 15 min buffer
        }
        
        return {
            day: day_number,
            activities,
            total_viewing_time: activities
                .filter(a => a.type === 'whale_viewing')
                .reduce((sum, a) => sum + a.duration_minutes, 0),
            total_travel_time: activities
                .filter(a => a.type === 'travel')
                .reduce((sum, a) => sum + a.duration_minutes, 0),
            expected_success_rate: this.calculateDaySuccessRate(activities)
        };
    }

    async generateContingencyPlans(detailed_routes, research_findings) {
        console.log('🛡️ Generating contingency plans...');
        
        const contingency_plans = [];
        
        for (const route of detailed_routes) {
            const contingencies = {
                weather_alternatives: await this.createWeatherAlternatives(route, research_findings),
                low_sighting_backups: this.createLowSightingBackups(route, research_findings),
                accessibility_alternatives: this.createAccessibilityAlternatives(route),
                timing_adjustments: this.createTimingAdjustments(route),
                emergency_procedures: this.createEmergencyProcedures(route)
            };
            
            contingency_plans.push({
                route_id: route.strategy,
                contingencies,
                activation_triggers: this.defineActivationTriggers(contingencies),
                priority_ranking: this.rankContingencies(contingencies)
            });
        }
        
        return contingency_plans;
    }

    compileRoutePlan(components) {
        console.log('📋 Compiling final route plan...');
        
        const {
            primary_routes,
            contingency_plans,
            research_evidence,
            sustainability_metrics
        } = components;
        
        return {
            // Executive summary
            executive_summary: this.generatePlanExecutiveSummary(components),
            
            // Route recommendations ranked by overall score
            recommended_routes: this.rankRoutes(primary_routes),
            
            // Contingency planning
            contingency_plans,
            
            // Supporting evidence
            research_evidence,
            
            // Sustainability analysis
            sustainability_analysis: sustainability_metrics,
            
            // Implementation guidance
            implementation_guide: this.createImplementationGuide(primary_routes),
            
            // Success metrics and KPIs
            success_metrics: this.defineSuccessMetrics(primary_routes),
            
            // Plan metadata
            plan_metadata: {
                generated_timestamp: new Date().toISOString(),
                plan_version: '2.0',
                agent_confidence: this.calculatePlanConfidence(primary_routes),
                estimated_preparation_time: '2-4 hours',
                plan_validity_period: '72 hours'
            }
        };
    }

    // Helper and utility methods
    calculateRouteSuccessRate(locations) {
        if (!locations || locations.length === 0) return 0.5;
        const avg_confidence = locations.reduce((sum, loc) => 
            sum + (loc.combined_confidence || 0.5), 0) / locations.length;
        return Math.min(0.95, avg_confidence * 1.1); // Slight boost for route synergy
    }

    calculateRouteDistance(locations, base) {
        let total_distance = 0;
        let current_point = base;
        
        for (const location of locations) {
            total_distance += this.calculateDistance(current_point, location.location);
            current_point = location.location;
        }
        
        // Return to base
        total_distance += this.calculateDistance(current_point, base);
        return total_distance;
    }

    calculateDistance(point1, point2) {
        // Haversine formula for distance calculation
        const R = 6371; // Earth's radius in km
        const dLat = (point2.lat - point1.lat) * Math.PI / 180;
        const dLng = (point2.lng - point1.lng) * Math.PI / 180;
        const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos(point1.lat * Math.PI / 180) * Math.cos(point2.lat * Math.PI / 180) *
                Math.sin(dLng/2) * Math.sin(dLng/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return R * c;
    }

    validateRouteConstraints(route, params) {
        // Validate that route meets planning constraints
        if (route.total_distance > params.max_daily_distance * params.trip_duration) {
            return false;
        }
        
        if (route.estimated_success_rate < 0.3) {
            return false; // Too low success probability
        }
        
        return true;
    }

    isAccessible(location, accessibility_needs) {
        // Check if location meets accessibility requirements
        if (!accessibility_needs || accessibility_needs.length === 0) return true;
        
        // Placeholder logic - would integrate with actual accessibility data
        return location.accessibility_rating !== 'poor';
    }

    // Fallback methods
    getFallbackPlan(constraints) {
        return {
            executive_summary: 'Fallback plan generated due to service limitations',
            recommended_routes: [{
                strategy: 'fallback',
                name: 'Basic Whale Watching Route',
                locations: [{
                    location: { lat: 48.5465, lng: -123.0307, name: 'Lime Kiln Point' },
                    combined_confidence: 0.75
                }],
                estimated_success_rate: 0.75
            }],
            plan_metadata: {
                generated_timestamp: new Date().toISOString(),
                agent_confidence: 0.6
            }
        };
    }

    cacheRoutePlan(constraints, plan) {
        const cache_key = JSON.stringify(constraints);
        this.route_cache.set(cache_key, {
            plan,
            timestamp: new Date(),
            expiry: new Date(Date.now() + 4 * 60 * 60 * 1000) // 4 hours
        });
    }

    // Placeholder implementations for complete functionality
    calculateSustainabilityScore(locations, params) { return 0.8; }
    solveTSP(locations) { return locations; } // Simplified TSP
    calculateTotalDistance(locations) { return 50; } // Placeholder
    calculateDisturbanceFactor(location) { return 0.2; }
    calculateMaxViewingDuration(location) { return 90; } // 90 minutes
    generateWelfareRecommendations(schedule) { return []; }
    minimizeEnvironmentalImpact(route, params) { return { score: 0.8 }; }
    maximizeCommunityBenefit(locations) { return { score: 0.7 }; }
    calculateImpactReduction(improvements) { return 0.15; }
    optimizeSequence(locations) { return locations; }
    calculateCarbonFootprint(route, params) { return 25; } // kg CO2
    summarizeTimeOptimization(schedules) { return { efficiency_gain: 0.15 }; }
    createLogisticsPlan(schedules) { return { transportation: 'car', meals: 'local' }; }
    calculateOptimalViewingDuration(location) { return 75; } // minutes
    calculateTravelTime(from, to) { return from ? 30 : 0; } // minutes
    addMinutes(time, minutes) { 
        const [h, m] = time.split(':').map(Number);
        const totalMinutes = h * 60 + m + minutes;
        const newH = Math.floor(totalMinutes / 60) % 24;
        const newM = totalMinutes % 60;
        return `${newH.toString().padStart(2, '0')}:${newM.toString().padStart(2, '0')}`;
    }
    calculateDaySuccessRate(activities) { return 0.8; }
    createWeatherAlternatives(route, research) { return []; }
    createLowSightingBackups(route, research) { return []; }
    createAccessibilityAlternatives(route) { return []; }
    createTimingAdjustments(route) { return []; }
    createEmergencyProcedures(route) { return []; }
    defineActivationTriggers(contingencies) { return {}; }
    rankContingencies(contingencies) { return []; }
    generatePlanExecutiveSummary(components) { return 'Route planning complete'; }
    rankRoutes(routes) { return routes.sort((a, b) => b.estimated_success_rate - a.estimated_success_rate); }
    createImplementationGuide(routes) { return { steps: [] }; }
    defineSuccessMetrics(routes) { return { target_success_rate: 0.8 }; }
    calculatePlanConfidence(routes) { return 0.85; }
    calculateSustainabilityMetrics(routes) { return { overall_score: 0.8 }; }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WhaleWatchingPlannerAgent;
}

// Make available globally
if (typeof window !== 'undefined') {
    window.WhaleWatchingPlannerAgent = WhaleWatchingPlannerAgent;
} 