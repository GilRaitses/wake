/**
 * Gemma 3 Whale Watching Integration
 * Connects SINDy + HMC research and planning agents to the existing Gemma 3 trip planner
 * 
 * This enhances the existing trip planner with scientific equation-based route optimization
 */

class Gemma3WhaleWatchingIntegration {
    constructor(config = {}) {
        // Connect to existing Gemma 3 system
        this.gemma3_planner = config.existingGemmaPlanner || window.agenticPlanner;
        this.multi_agent_orchestrator = config.orchestrator || window.multiAgentOrchestrator;
        
        // Initialize our scientific agents
        this.research_agent = new WhaleWatchingResearchAgent({
            sindyServiceUrl: config.sindyServiceUrl || '/api/sindy-predictions',
            hmcServiceUrl: config.hmcServiceUrl || '/api/hmc-uncertainty',
            firestoreDB: config.firestoreDB
        });
        
        this.planner_agent = new WhaleWatchingPlannerAgent({
            researchAgent: this.research_agent,
            googleMapsAPI: config.googleMapsAPI
        });
        
        // Integration state
        this.current_research = null;
        this.current_plan = null;
        this.enhancement_active = true;
        
        console.log('🌊 Gemma 3 Whale Watching Integration initialized');
        this.integrateWithExistingSystem();
    }

    /**
     * MAIN INTEGRATION METHODS
     */

    integrateWithExistingSystem() {
        // Hook into existing Gemma 3 trip planning flow
        if (this.gemma3_planner && typeof this.gemma3_planner.planTrip === 'function') {
            this.enhanceGemma3Planning();
        }
        
        if (this.multi_agent_orchestrator) {
            this.integrateWithOrchestrator();
        }
        
        // Add scientific enhancement UI controls
        this.addScientificEnhancementControls();
    }

    enhanceGemma3Planning() {
        // Store original planning method
        const original_planTrip = this.gemma3_planner.planTrip.bind(this.gemma3_planner);
        
        // Enhance with scientific agents
        this.gemma3_planner.planTrip = async (userInput, options = {}) => {
            console.log('🧬 Enhancing Gemma 3 planning with SINDy + HMC science...');
            
            try {
                // Step 1: Get original Gemma 3 plan
                const gemma3_plan = await original_planTrip(userInput, options);
                
                // Step 2: Extract constraints for scientific analysis
                const scientific_constraints = this.extractConstraintsFromGemma3Plan(gemma3_plan, userInput);
                
                // Step 3: Run scientific research using SINDy equations
                console.log('🔬 Running SINDy equation research...');
                const research_findings = await this.research_agent.researchOptimalViewingLocations(scientific_constraints);
                
                // Step 4: Generate scientifically-optimized routes
                console.log('📋 Creating science-based route plans...');
                const scientific_route_plan = await this.planner_agent.planSustainableViewingRoutes(scientific_constraints, research_findings);
                
                // Step 5: Merge Gemma 3 intelligence with scientific evidence
                const enhanced_plan = this.mergeGemma3WithScience(gemma3_plan, research_findings, scientific_route_plan);
                
                // Step 6: Store for reference
                this.current_research = research_findings;
                this.current_plan = scientific_route_plan;
                
                console.log('✨ Enhanced plan with scientific evidence ready');
                return enhanced_plan;
                
            } catch (error) {
                console.error('Scientific enhancement error:', error);
                // Fallback to original Gemma 3 plan
                return await original_planTrip(userInput, options);
            }
        };
    }

    extractConstraintsFromGemma3Plan(gemma3_plan, userInput) {
        // Extract planning constraints from Gemma 3's analysis
        const constraints = {
            // Temporal constraints from Gemma 3
            dates: {
                start: gemma3_plan.startDate || new Date(),
                end: gemma3_plan.endDate || new Date(Date.now() + 3 * 24 * 60 * 60 * 1000)
            },
            
            // Spatial constraints
            region: gemma3_plan.region || 'san_juan_islands',
            max_distance: gemma3_plan.maxDistance || 50, // km
            
            // Group constraints
            group_size: gemma3_plan.groupSize || 2,
            experience_level: gemma3_plan.experienceLevel || 'intermediate',
            
            // Preferences from Gemma 3 analysis
            viewing_mode: gemma3_plan.viewingMode || 'flexible', // boat, shore, kayak
            sustainability_priority: gemma3_plan.sustainability || 'moderate',
            budget: gemma3_plan.budget || 500,
            
            // Accessibility requirements
            accessibility: gemma3_plan.accessibility || 'standard',
            mobility_assistance: gemma3_plan.mobilityAssistance || false,
            
            // Experience preferences
            photography_focus: gemma3_plan.photographyFocus || false,
            education_priority: gemma3_plan.educationPriority || 'moderate',
            wildlife_interests: gemma3_plan.wildlifeInterests || ['whales'],
            
            // Scientific research priorities
            research_contribution: gemma3_plan.researchContribution || false,
            data_collection: gemma3_plan.dataCollection || false
        };
        
        return constraints;
    }

    mergeGemma3WithScience(gemma3_plan, research_findings, scientific_route_plan) {
        // Merge Gemma 3's trip intelligence with scientific evidence
        const enhanced_plan = {
            // Preserve Gemma 3's core planning
            original_gemma3_plan: gemma3_plan,
            
            // Add scientific enhancements
            scientific_research: research_findings,
            optimized_routes: scientific_route_plan,
            
            // Create unified recommendations
            unified_recommendations: this.createUnifiedRecommendations(
                gemma3_plan, research_findings, scientific_route_plan
            ),
            
            // Enhanced trip structure
            enhanced_itinerary: this.createEnhancedItinerary(
                gemma3_plan.itinerary, scientific_route_plan.primary_routes
            ),
            
            // Scientific confidence metrics
            confidence_analysis: {
                gemma3_confidence: gemma3_plan.confidence || 0.75,
                scientific_confidence: research_findings.confidence || 0.80,
                combined_confidence: this.calculateCombinedConfidence(
                    gemma3_plan.confidence || 0.75,
                    research_findings.confidence || 0.80
                )
            },
            
            // Evidence-based explanations
            scientific_explanations: this.generateScientificExplanations(research_findings),
            
            // Optimization insights
            optimization_insights: this.generateOptimizationInsights(scientific_route_plan)
        };
        
        return enhanced_plan;
    }

    createUnifiedRecommendations(gemma3_plan, research_findings, route_plan) {
        // Combine Gemma 3's recommendations with scientific insights
        const unified = {
            // Primary recommendations (highest confidence)
            primary_recommendations: [],
            
            // Alternative options
            alternatives: [],
            
            // Scientific backing
            evidence_support: []
        };
        
        // Add Gemma 3 recommendations with scientific validation
        if (gemma3_plan.recommendations) {
            gemma3_plan.recommendations.forEach(rec => {
                const scientific_support = this.validateRecommendationWithScience(rec, research_findings);
                
                unified.primary_recommendations.push({
                    recommendation: rec,
                    source: 'gemma3',
                    scientific_support: scientific_support,
                    confidence: scientific_support.confidence
                });
            });
        }
        
        // Add scientific recommendations not covered by Gemma 3
        if (research_findings.top_recommendations) {
            research_findings.top_recommendations.primary_locations.forEach(loc => {
                if (!this.isLocationCoveredByGemma3(loc, gemma3_plan)) {
                    unified.primary_recommendations.push({
                        recommendation: `Visit ${loc.name} during ${loc.optimal_time}`,
                        source: 'scientific_research',
                        scientific_support: {
                            sindy_evidence: loc.sindy_predictions,
                            confidence: loc.confidence
                        },
                        confidence: loc.confidence
                    });
                }
            });
        }
        
        return unified;
    }

    createEnhancedItinerary(gemma3_itinerary, scientific_routes) {
        // Merge Gemma 3 itinerary with scientifically-optimized routes
        const enhanced_days = [];
        
        if (gemma3_itinerary && gemma3_itinerary.days) {
            gemma3_itinerary.days.forEach((day, index) => {
                const scientific_route = scientific_routes[index] || scientific_routes[0];
                
                enhanced_days.push({
                    day: day.day,
                    gemma3_plan: day,
                    scientific_optimization: scientific_route,
                    
                    // Merged activities
                    optimized_activities: this.mergeActivities(day.activities, scientific_route.activities),
                    
                    // Timing optimization
                    optimal_timing: scientific_route.timing,
                    
                    // Success probability
                    success_probability: scientific_route.success_probability,
                    
                    // Environmental considerations
                    environmental_factors: scientific_route.environmental_factors
                });
            });
        }
        
        return {
            days: enhanced_days,
            total_days: enhanced_days.length,
            overall_success_probability: this.calculateOverallSuccessProbability(enhanced_days)
        };
    }

    integrateWithOrchestrator() {
        // Integrate with multi-agent orchestrator if available
        if (this.multi_agent_orchestrator) {
            // Register our agents with the orchestrator
            this.multi_agent_orchestrator.registerAgent('whale_research', this.research_agent);
            this.multi_agent_orchestrator.registerAgent('whale_planner', this.planner_agent);
            
            // Set up event listeners for orchestrator coordination
            this.multi_agent_orchestrator.on('planning_requested', async (event) => {
                await this.handleOrchestatedPlanning(event);
            });
        }
    }

    addScientificEnhancementControls() {
        // Add UI controls for scientific enhancement features
        if (typeof document !== 'undefined') {
            this.addEnhancementToggle();
            this.addScientificMetricsDisplay();
            this.addResearchExportFeatures();
        }
    }

    /**
     * HELPER METHODS
     */

    validateRecommendationWithScience(recommendation, research_findings) {
        // Validate Gemma 3 recommendation against scientific research
        let scientific_support = {
            validated: false,
            confidence: 0.5,
            evidence: []
        };
        
        // Check if recommendation aligns with research findings
        if (research_findings.top_recommendations) {
            const matching_location = research_findings.top_recommendations.primary_locations.find(
                loc => recommendation.toLowerCase().includes(loc.name.toLowerCase())
            );
            
            if (matching_location) {
                scientific_support = {
                    validated: true,
                    confidence: matching_location.confidence,
                    evidence: [
                        `SINDy equation predictions support this location`,
                        `Historical success rate: ${matching_location.success_rate}`,
                        `Optimal viewing time: ${matching_location.optimal_time}`
                    ]
                };
            }
        }
        
        return scientific_support;
    }

    isLocationCoveredByGemma3(scientific_location, gemma3_plan) {
        // Check if scientific location is already covered by Gemma 3 plan
        if (!gemma3_plan.locations) return false;
        
        return gemma3_plan.locations.some(loc => 
            loc.name.toLowerCase().includes(scientific_location.name.toLowerCase()) ||
            scientific_location.name.toLowerCase().includes(loc.name.toLowerCase())
        );
    }

    mergeActivities(gemma3_activities, scientific_activities) {
        // Merge activities from both sources
        const merged = [...(gemma3_activities || [])];
        
        if (scientific_activities) {
            scientific_activities.forEach(sci_activity => {
                if (!merged.find(act => act.name === sci_activity.name)) {
                    merged.push({
                        ...sci_activity,
                        source: 'scientific_optimization'
                    });
                }
            });
        }
        
        return merged;
    }

    calculateCombinedConfidence(gemma3_confidence, scientific_confidence) {
        // Calculate combined confidence using weighted average
        const gemma3_weight = 0.4; // Gemma 3 general intelligence
        const scientific_weight = 0.6; // Scientific evidence weight
        
        return (gemma3_confidence * gemma3_weight) + (scientific_confidence * scientific_weight);
    }

    calculateOverallSuccessProbability(enhanced_days) {
        // Calculate overall success probability for the trip
        if (!enhanced_days || enhanced_days.length === 0) return 0.5;
        
        const daily_probabilities = enhanced_days.map(day => day.success_probability || 0.5);
        return daily_probabilities.reduce((sum, prob) => sum + prob, 0) / daily_probabilities.length;
    }

    generateScientificExplanations(research_findings) {
        // Generate user-friendly explanations of scientific evidence
        const explanations = [];
        
        if (research_findings.sindy_insights) {
            explanations.push({
                type: 'mathematical_model',
                title: 'SINDy Equation Analysis',
                explanation: 'Advanced mathematical models identify optimal whale viewing locations based on environmental patterns and historical sighting data.',
                confidence: research_findings.sindy_insights.confidence || 0.8
            });
        }
        
        if (research_findings.uncertainty_analysis) {
            explanations.push({
                type: 'uncertainty_quantification',
                title: 'Uncertainty Analysis',
                explanation: 'Bayesian uncertainty analysis provides confidence intervals for predictions, helping you understand the reliability of recommendations.',
                confidence: research_findings.uncertainty_analysis.confidence || 0.75
            });
        }
        
        return explanations;
    }

    generateOptimizationInsights(route_plan) {
        // Generate insights about route optimization
        const insights = [];
        
        if (route_plan.sustainability_metrics) {
            insights.push({
                category: 'sustainability',
                insight: `Routes optimized for ${route_plan.sustainability_metrics.environmental_impact_reduction}% reduced environmental impact`,
                benefit: 'Supports whale conservation while enhancing viewing opportunities'
            });
        }
        
        if (route_plan.timing_optimization) {
            insights.push({
                category: 'timing',
                insight: `Optimal timing increases success probability by ${route_plan.timing_optimization.improvement_percentage}%`,
                benefit: 'Maximizes whale viewing opportunities'
            });
        }
        
        return insights;
    }

    /**
     * UI ENHANCEMENT METHODS
     */

    addEnhancementToggle() {
        // Add toggle for scientific enhancement
        const toggle = document.createElement('div');
        toggle.innerHTML = `
            <label>
                <input type="checkbox" id="scientific-enhancement-toggle" ${this.enhancement_active ? 'checked' : ''}>
                Enable Scientific Enhancement
            </label>
        `;
        
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.appendChild(toggle);
            
            document.getElementById('scientific-enhancement-toggle').addEventListener('change', (e) => {
                this.enhancement_active = e.target.checked;
                console.log(`Scientific enhancement ${this.enhancement_active ? 'enabled' : 'disabled'}`);
            });
        }
    }

    addScientificMetricsDisplay() {
        // Add display for scientific metrics
        const metricsPanel = document.createElement('div');
        metricsPanel.id = 'scientific-metrics';
        metricsPanel.innerHTML = `
            <h4>Scientific Analysis</h4>
            <div id="sindy-confidence">SINDy Confidence: --</div>
            <div id="hmc-uncertainty">HMC Uncertainty: --</div>
            <div id="research-quality">Research Quality: --</div>
        `;
        
        const floatingPanel = document.querySelector('.floating-panel');
        if (floatingPanel) {
            floatingPanel.appendChild(metricsPanel);
        }
    }

    addResearchExportFeatures() {
        // Add research data export features
        const exportPanel = document.createElement('div');
        exportPanel.innerHTML = `
            <button onclick="window.gemma3Integration.exportResearchData()">
                Export Research Data
            </button>
            <button onclick="window.gemma3Integration.exportRouteOptimization()">
                Export Route Analysis
            </button>
        `;
        
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.appendChild(exportPanel);
        }
    }

    /**
     * EXPORT METHODS
     */

    exportResearchData() {
        // Export current research data
        if (this.current_research) {
            const exportData = {
                timestamp: new Date().toISOString(),
                research_findings: this.current_research,
                confidence_metrics: this.current_research.confidence_analysis,
                sindy_insights: this.current_research.sindy_insights
            };
            
            this.downloadJSON(exportData, 'whale-research-data.json');
        }
    }

    exportRouteOptimization() {
        // Export route optimization data
        if (this.current_plan) {
            const exportData = {
                timestamp: new Date().toISOString(),
                route_plan: this.current_plan,
                optimization_metrics: this.current_plan.sustainability_metrics,
                success_probabilities: this.current_plan.success_analysis
            };
            
            this.downloadJSON(exportData, 'whale-route-optimization.json');
        }
    }

    downloadJSON(data, filename) {
        // Utility method to download JSON data
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        
        URL.revokeObjectURL(url);
    }

    /**
     * PUBLIC API METHODS
     */

    async executeEnhancedPlanning(userInput, options = {}) {
        // Public method for enhanced planning
        if (!this.enhancement_active) {
            console.log('Scientific enhancement disabled, using standard planning');
            return null;
        }
        
        try {
            const constraints = this.extractConstraintsFromUserInput(userInput);
            const research = await this.research_agent.researchOptimalViewingLocations(constraints);
            const plan = await this.planner_agent.planSustainableViewingRoutes(constraints, research);
            
            return {
                research: research,
                plan: plan,
                confidence: this.calculateCombinedConfidence(0.75, research.confidence || 0.8)
            };
            
        } catch (error) {
            console.error('Enhanced planning failed:', error);
            return null;
        }
    }

    extractConstraintsFromUserInput(userInput) {
        // Extract constraints from raw user input
        return {
            dates: this.extractDatesFromInput(userInput),
            group_size: this.extractGroupSizeFromInput(userInput),
            preferences: this.extractPreferencesFromInput(userInput)
        };
    }

    extractDatesFromInput(input) {
        // Simple date extraction - enhance with NLP
        const dateRegex = /(\d{1,2}\/\d{1,2}\/\d{4})/g;
        return input.match(dateRegex) || [];
    }

    extractGroupSizeFromInput(input) {
        // Extract group size from input
        const sizeRegex = /(\d+)\s*(people|person)/i;
        const match = input.match(sizeRegex);
        return match ? parseInt(match[1]) : 2;
    }

    extractPreferencesFromInput(input) {
        // Extract preferences from input
        const prefs = {};
        
        if (input.toLowerCase().includes('boat')) prefs.viewing_mode = 'boat';
        if (input.toLowerCase().includes('shore')) prefs.viewing_mode = 'shore';
        if (input.toLowerCase().includes('photo')) prefs.photography = true;
        if (input.toLowerCase().includes('sustainable')) prefs.sustainability = 'high';
        
        return prefs;
    }
}

// Make available globally
if (typeof window !== 'undefined') {
    window.Gemma3WhaleWatchingIntegration = Gemma3WhaleWatchingIntegration;
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Gemma3WhaleWatchingIntegration;
} 