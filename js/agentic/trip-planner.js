/**
 * ORCAST Agentic Trip Planner
 * AI-powered whale watching trip planning with voice input and multi-dimensional optimization
 */

class AgenticTripPlanner {
    constructor() {
        this.isListening = false;
        this.speechRecognition = null;
        this.currentPlan = null;
        this.userConstraints = {};
        this.locations = [];
        
        this.initializeSpeechRecognition();
        this.initializeGeminiAPI();
        this.loadLocationData();
    }

    /**
     * Initialize Web Speech API for voice input
     */
    initializeSpeechRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.speechRecognition = new SpeechRecognition();
            
            this.speechRecognition.continuous = true;
            this.speechRecognition.interimResults = true;
            this.speechRecognition.lang = 'en-US';
            
            this.speechRecognition.onstart = () => {
                this.isListening = true;
                this.updateVoiceUI('listening');
            };
            
            this.speechRecognition.onresult = (event) => {
                const transcript = Array.from(event.results)
                    .map(result => result[0].transcript)
                    .join('');
                
                this.updateVoiceUI('processing', transcript);
                this.processVoiceInput(transcript);
            };
            
            this.speechRecognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.updateVoiceUI('error', event.error);
            };
            
            this.speechRecognition.onend = () => {
                this.isListening = false;
                this.updateVoiceUI('ready');
            };
        } else {
            console.warn('Speech recognition not supported in this browser');
        }
    }

    /**
     * Initialize Gemini API for natural language processing
     */
    initializeGeminiAPI() {
        // Note: In production, this would use your actual Gemini API key
        this.geminiEndpoint = '/api/gemini/analyze';
        this.geminiHeaders = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${window.ORCASTConfig?.gemini?.apiKey || 'demo-key'}`
        };
    }

    /**
     * Load orca viewing location data
     */
    loadLocationData() {
        // Load from existing ORCAST data
        if (window.orcaSightings && window.probabilityGrid) {
            this.locations = this.extractViewingLocations();
        } else {
            // Load location data
            this.loadOrcaData();
        }
    }

    /**
     * Start voice input for trip planning
     */
    startVoicePlanning() {
        if (!this.speechRecognition) {
            alert('Voice input not supported. Please use text input.');
            return;
        }

        if (this.isListening) {
            this.speechRecognition.stop();
        } else {
            this.speechRecognition.start();
        }
    }

    /**
     * Process voice input and extract planning constraints
     */
    async processVoiceInput(transcript) {
        try {
            // Send to Gemini API for constraint extraction
            const constraints = await this.extractConstraintsWithGemini(transcript);
            
            // Update user constraints
            this.userConstraints = { ...this.userConstraints, ...constraints };
            
            // Generate trip plan
            if (this.hasMinimumConstraints(constraints)) {
                const plan = await this.generateTripPlan(this.userConstraints);
                this.displayTripPlan(plan);
            } else {
                this.askForMoreDetails(constraints);
            }
            
        } catch (error) {
            console.error('Error processing voice input:', error);
            this.displayError('Error processing your request. Please try again.');
        }
    }

    /**
     * Extract planning constraints using Gemini API
     */
    async extractConstraintsWithGemini(text) {
        // For MVP, use rule-based extraction with Gemini simulation
        const constraints = this.extractConstraintsRuleBased(text);
        
        // TODO: Replace with actual Gemini API call
        // const response = await fetch(this.geminiEndpoint, {
        //     method: 'POST',
        //     headers: this.geminiHeaders,
        //     body: JSON.stringify({
        //         prompt: `Extract trip planning constraints from: "${text}"`,
        //         format: 'json'
        //     })
        // });
        
        return constraints;
    }

    /**
     * Rule-based constraint extraction (MVP implementation)
     */
    extractConstraintsRuleBased(text) {
        const constraints = {};
        const lowerText = text.toLowerCase();
        
        // Time constraints
        if (lowerText.includes('weekend')) {
            constraints.timeframe = 'weekend';
        }
        if (lowerText.includes('morning')) {
            constraints.preferredTime = 'morning';
        }
        if (lowerText.includes('afternoon')) {
            constraints.preferredTime = 'afternoon';
        }
        
        // Duration
        const durationMatch = lowerText.match(/(\d+)\s?(day|days)/);
        if (durationMatch) {
            constraints.duration = parseInt(durationMatch[1]);
        }
        
        // Viewing preferences
        if (lowerText.includes('land') || lowerText.includes('shore')) {
            constraints.viewingType = 'land';
        }
        if (lowerText.includes('boat') || lowerText.includes('ferry')) {
            constraints.viewingType = 'boat';
        }
        if (lowerText.includes('balcony')) {
            constraints.accommodation = 'balcony';
        }
        
        // Location preferences
        if (lowerText.includes('san juan')) {
            constraints.region = 'san_juan_islands';
        }
        if (lowerText.includes('seattle')) {
            constraints.region = 'puget_sound';
        }
        
        return constraints;
    }

    /**
     * Generate multi-dimensional trip plan
     */
    async generateTripPlan(constraints) {
        const plan = {
            id: Date.now(),
            created: new Date().toISOString(),
            constraints: constraints,
            timeline: [],
            locations: [],
            logistics: {},
            alternatives: [],
            probabilityScore: 0
        };

        // Find optimal locations based on constraints
        const optimalLocations = this.findOptimalLocations(constraints);
        plan.locations = optimalLocations;

        // Generate timeline
        plan.timeline = this.generateTimeline(constraints, optimalLocations);

        // Add logistics
        plan.logistics = this.generateLogistics(constraints, optimalLocations);

        // Calculate overall probability score
        plan.probabilityScore = this.calculatePlanProbability(plan);

        // Generate alternatives
        plan.alternatives = this.generateAlternatives(plan);

        return plan;
    }

    /**
     * Find optimal viewing locations based on constraints
     */
    findOptimalLocations(constraints) {
        let locations = [...this.locations];

        // Filter by viewing type
        if (constraints.viewingType === 'land') {
            locations = locations.filter(loc => loc.landViewing);
        }

        // Filter by region
        if (constraints.region) {
            locations = locations.filter(loc => loc.region === constraints.region);
        }

        // Sort by probability and convenience
        locations.sort((a, b) => {
            const scoreA = this.calculateLocationScore(a, constraints);
            const scoreB = this.calculateLocationScore(b, constraints);
            return scoreB - scoreA;
        });

        // Return top locations based on duration
        const maxLocations = constraints.duration ? Math.min(constraints.duration * 2, 6) : 3;
        return locations.slice(0, maxLocations);
    }

    /**
     * Calculate location score based on constraints
     */
    calculateLocationScore(location, constraints) {
        let score = location.probabilityScore || 0.5;

        // Time preference bonus
        if (constraints.preferredTime && location.bestTimes?.includes(constraints.preferredTime)) {
            score += 0.2;
        }

        // Accessibility bonus
        if (constraints.accommodation === 'balcony' && location.balconyAccommodations) {
            score += 0.15;
        }

        // Weather reliability
        score += (location.weatherReliability || 0.5) * 0.1;

        return score;
    }

    /**
     * Generate day-by-day timeline
     */
    generateTimeline(constraints, locations) {
        const timeline = [];
        const duration = constraints.duration || 1;
        const preferredTime = constraints.preferredTime || 'morning';

        for (let day = 1; day <= duration; day++) {
            const dayPlan = {
                day: day,
                date: this.calculateDate(day),
                schedule: []
            };

            // Primary viewing location
            const location = locations[Math.min(day - 1, locations.length - 1)];
            
            if (preferredTime === 'morning' || preferredTime === 'all-day') {
                dayPlan.schedule.push({
                    time: '6:00 AM - 10:00 AM',
                    activity: 'Orca Watching',
                    location: location.name,
                    probabilityScore: location.probabilityScore,
                    details: 'Prime viewing hours with highest orca activity'
                });
            }

            if (preferredTime === 'afternoon' || preferredTime === 'all-day') {
                dayPlan.schedule.push({
                    time: '2:00 PM - 6:00 PM',
                    activity: 'Orca Watching',
                    location: location.name,
                    probabilityScore: location.probabilityScore * 0.8,
                    details: 'Afternoon viewing with good lighting'
                });
            }

            // Add meals and rest
            dayPlan.schedule.push({
                time: '12:00 PM - 1:00 PM',
                activity: 'Lunch',
                location: location.nearbyDining?.[0] || 'Local restaurant',
                details: 'Meal break with ocean view if available'
            });

            timeline.push(dayPlan);
        }

        return timeline;
    }

    /**
     * Generate logistics (accommodation, transportation, etc.)
     */
    generateLogistics(constraints, locations) {
        const logistics = {
            accommodation: [],
            transportation: [],
            dining: [],
            equipment: []
        };

        // Accommodation suggestions
        if (constraints.accommodation === 'balcony') {
            logistics.accommodation = locations
                .filter(loc => loc.balconyAccommodations)
                .map(loc => ({
                    name: loc.balconyAccommodations[0],
                    location: loc.name,
                    features: ['Ocean view balcony', 'Whale watching friendly'],
                    bookingUrl: '#'
                }));
        }

        // Transportation
        logistics.transportation.push({
            type: 'Car rental',
            recommendation: 'Recommended for flexibility between viewing locations',
            alternatives: ['Ferry system', 'Local shuttle services']
        });

        // Equipment recommendations
        logistics.equipment = [
            'Binoculars (8x42 recommended)',
            'Camera with telephoto lens',
            'Weather-appropriate clothing',
            'Snacks and water',
            'Portable chair (for land viewing)'
        ];

        return logistics;
    }

    /**
     * Calculate overall plan probability score
     */
    calculatePlanProbability(plan) {
        if (!plan.locations.length) return 0;

        const locationScores = plan.locations.map(loc => loc.probabilityScore || 0.5);
        const averageScore = locationScores.reduce((sum, score) => sum + score, 0) / locationScores.length;

        // Adjust for weather, season, and other factors
        const seasonAdjustment = this.getSeasonAdjustment();
        const weatherAdjustment = 0.9; // TODO: Get from weather API

        return Math.min(averageScore * seasonAdjustment * weatherAdjustment, 1.0);
    }

    /**
     * Display generated trip plan
     */
    displayTripPlan(plan) {
        this.currentPlan = plan;
        
        const planContainer = document.getElementById('trip-plan-display');
        if (!planContainer) return;

        planContainer.innerHTML = `
            <div class="trip-plan">
                <div class="plan-header">
                    <h3>Your Orca Watching Trip Plan</h3>
                    <div class="probability-score">
                        <span class="score">${(plan.probabilityScore * 100).toFixed(0)}%</span>
                        <span class="label">Success Probability</span>
                    </div>
                </div>
                
                <div class="plan-timeline">
                    ${plan.timeline.map(day => this.renderDayPlan(day)).join('')}
                </div>
                
                <div class="plan-logistics">
                    <h4>Logistics & Recommendations</h4>
                    ${this.renderLogistics(plan.logistics)}
                </div>
                
                <div class="plan-actions">
                    <button onclick="agenticPlanner.exportPlan('email')" class="btn-primary">
                        📧 Email Plan
                    </button>
                    <button onclick="agenticPlanner.exportPlan('calendar')" class="btn-secondary">
                        📅 Add to Calendar
                    </button>
                    <button onclick="agenticPlanner.sharePlan()" class="btn-secondary">
                        🔗 Share Plan
                    </button>
                </div>
            </div>
        `;
        
        planContainer.style.display = 'block';
    }

    /**
     * Render individual day plan
     */
    renderDayPlan(day) {
        return `
            <div class="day-plan">
                <h4>Day ${day.day} - ${new Date(day.date).toLocaleDateString()}</h4>
                <div class="schedule">
                    ${day.schedule.map(item => `
                        <div class="schedule-item">
                            <div class="time">${item.time}</div>
                            <div class="activity">
                                <strong>${item.activity}</strong>
                                <div class="location">${item.location}</div>
                                ${item.probabilityScore ? `
                                    <div class="probability">${(item.probabilityScore * 100).toFixed(0)}% chance</div>
                                ` : ''}
                                <div class="details">${item.details}</div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    /**
     * Export plan in various formats
     */
    async exportPlan(format) {
        if (!this.currentPlan) return;

        switch (format) {
            case 'email':
                this.exportToEmail();
                break;
            case 'calendar':
                this.exportToCalendar();
                break;
            case 'pdf':
                this.exportToPDF();
                break;
        }
    }

    /**
     * Export plan to email
     */
    exportToEmail() {
        const plan = this.currentPlan;
        const subject = `Your ORCAST Orca Watching Trip Plan`;
        const body = this.generateEmailContent(plan);
        
        const mailtoLink = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
        window.open(mailtoLink);
    }

    /**
     * Generate email content
     */
    generateEmailContent(plan) {
        return `
Your ORCAST Orca Watching Trip Plan
Success Probability: ${(plan.probabilityScore * 100).toFixed(0)}%

TIMELINE:
${plan.timeline.map(day => `
Day ${day.day} - ${new Date(day.date).toLocaleDateString()}
${day.schedule.map(item => `• ${item.time}: ${item.activity} at ${item.location}`).join('\n')}
`).join('\n')}

EQUIPMENT CHECKLIST:
${plan.logistics.equipment?.map(item => `☐ ${item}`).join('\n') || 'No equipment specified'}

CONTACTS & BOOKINGS:
• Accommodation: Contact details for reservations
• Transportation: Rental or ferry information
• Emergency: Local marine mammal rescue: (555) 123-4567

Generated by ORCAST - Optimizing your orca watching experience
Visit: https://orcast.org
        `.trim();
    }

    /**
     * Update voice UI status
     */
    updateVoiceUI(status, message = '') {
        const voiceButton = document.getElementById('voice-planning-btn');
        const voiceStatus = document.getElementById('voice-status');
        const voiceTranscript = document.getElementById('voice-transcript');

        if (voiceButton) {
            voiceButton.className = `voice-btn ${status}`;
            voiceButton.innerHTML = this.getVoiceButtonContent(status);
        }

        if (voiceStatus) {
            voiceStatus.textContent = this.getVoiceStatusText(status);
        }

        if (voiceTranscript && message) {
            voiceTranscript.textContent = message;
        }
    }

    /**
     * Get voice button content based on status
     */
    getVoiceButtonContent(status) {
        switch (status) {
            case 'listening': return '🎤 Listening...';
            case 'processing': return '🧠 Processing...';
            case 'error': return '❌ Error';
            default: return '🎤 Start Voice Planning';
        }
    }

    /**
     * Get helper methods
     */
    hasMinimumConstraints(constraints) {
        return Object.keys(constraints).length >= 2;
    }

    calculateDate(dayOffset) {
        const date = new Date();
        date.setDate(date.getDate() + dayOffset);
        return date.toISOString();
    }

    getSeasonAdjustment() {
        const month = new Date().getMonth();
        // Summer months have higher orca activity
        if (month >= 5 && month <= 8) return 1.0;
        if (month >= 3 && month <= 10) return 0.8;
        return 0.6;
    }

    extractViewingLocations() {
        // Extract unique viewing locations from orca sightings data
        // This would integrate with existing ORCAST data
        return [
            {
                name: 'Lime Kiln Point State Park',
                region: 'san_juan_islands',
                landViewing: true,
                probabilityScore: 0.85,
                bestTimes: ['morning', 'afternoon'],
                balconyAccommodations: ['Friday Harbor House', 'Earthbox Motel'],
                nearbyDining: ['Coho Restaurant', 'Market Chef'],
                weatherReliability: 0.9
            },
            {
                name: 'Deception Pass Bridge',
                region: 'puget_sound',
                landViewing: true,
                probabilityScore: 0.65,
                bestTimes: ['morning'],
                balconyAccommodations: ['Captain Whidbey Inn'],
                nearbyDining: ['Deception Pass Cafe'],
                weatherReliability: 0.8
            },
            {
                name: 'Mukilteo Lighthouse Park',
                region: 'puget_sound',
                landViewing: true,
                probabilityScore: 0.55,
                bestTimes: ['afternoon'],
                balconyAccommodations: ['Silver Cloud Hotel'],
                nearbyDining: ['Ivars Mukilteo Landing'],
                weatherReliability: 0.7
            }
        ];
    }

    // Additional helper methods would go here...
}

// Initialize global agentic planner
window.agenticPlanner = new AgenticTripPlanner(); 
 * ORCAST Agentic Trip Planner
 * AI-powered whale watching trip planning with voice input and multi-dimensional optimization
 */

class AgenticTripPlanner {
    constructor() {
        this.isListening = false;
        this.speechRecognition = null;
        this.currentPlan = null;
        this.userConstraints = {};
        this.locations = [];
        
        this.initializeSpeechRecognition();
        this.initializeGeminiAPI();
        this.loadLocationData();
    }

    /**
     * Initialize Web Speech API for voice input
     */
    initializeSpeechRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.speechRecognition = new SpeechRecognition();
            
            this.speechRecognition.continuous = true;
            this.speechRecognition.interimResults = true;
            this.speechRecognition.lang = 'en-US';
            
            this.speechRecognition.onstart = () => {
                this.isListening = true;
                this.updateVoiceUI('listening');
            };
            
            this.speechRecognition.onresult = (event) => {
                const transcript = Array.from(event.results)
                    .map(result => result[0].transcript)
                    .join('');
                
                this.updateVoiceUI('processing', transcript);
                this.processVoiceInput(transcript);
            };
            
            this.speechRecognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.updateVoiceUI('error', event.error);
            };
            
            this.speechRecognition.onend = () => {
                this.isListening = false;
                this.updateVoiceUI('ready');
            };
        } else {
            console.warn('Speech recognition not supported in this browser');
        }
    }

    /**
     * Initialize Gemini API for natural language processing
     */
    initializeGeminiAPI() {
        // Note: In production, this would use your actual Gemini API key
        this.geminiEndpoint = '/api/gemini/analyze';
        this.geminiHeaders = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${window.ORCASTConfig?.gemini?.apiKey || 'demo-key'}`
        };
    }

    /**
     * Load orca viewing location data
     */
    loadLocationData() {
        // Load from existing ORCAST data
        if (window.orcaSightings && window.probabilityGrid) {
            this.locations = this.extractViewingLocations();
        } else {
            // Load location data
            this.loadOrcaData();
        }
    }

    /**
     * Start voice input for trip planning
     */
    startVoicePlanning() {
        if (!this.speechRecognition) {
            alert('Voice input not supported. Please use text input.');
            return;
        }

        if (this.isListening) {
            this.speechRecognition.stop();
        } else {
            this.speechRecognition.start();
        }
    }

    /**
     * Process voice input and extract planning constraints
     */
    async processVoiceInput(transcript) {
        try {
            // Send to Gemini API for constraint extraction
            const constraints = await this.extractConstraintsWithGemini(transcript);
            
            // Update user constraints
            this.userConstraints = { ...this.userConstraints, ...constraints };
            
            // Generate trip plan
            if (this.hasMinimumConstraints(constraints)) {
                const plan = await this.generateTripPlan(this.userConstraints);
                this.displayTripPlan(plan);
            } else {
                this.askForMoreDetails(constraints);
            }
            
        } catch (error) {
            console.error('Error processing voice input:', error);
            this.displayError('Error processing your request. Please try again.');
        }
    }

    /**
     * Extract planning constraints using Gemini API
     */
    async extractConstraintsWithGemini(text) {
        // For MVP, use rule-based extraction with Gemini simulation
        const constraints = this.extractConstraintsRuleBased(text);
        
        // TODO: Replace with actual Gemini API call
        // const response = await fetch(this.geminiEndpoint, {
        //     method: 'POST',
        //     headers: this.geminiHeaders,
        //     body: JSON.stringify({
        //         prompt: `Extract trip planning constraints from: "${text}"`,
        //         format: 'json'
        //     })
        // });
        
        return constraints;
    }

    /**
     * Rule-based constraint extraction (MVP implementation)
     */
    extractConstraintsRuleBased(text) {
        const constraints = {};
        const lowerText = text.toLowerCase();
        
        // Time constraints
        if (lowerText.includes('weekend')) {
            constraints.timeframe = 'weekend';
        }
        if (lowerText.includes('morning')) {
            constraints.preferredTime = 'morning';
        }
        if (lowerText.includes('afternoon')) {
            constraints.preferredTime = 'afternoon';
        }
        
        // Duration
        const durationMatch = lowerText.match(/(\d+)\s?(day|days)/);
        if (durationMatch) {
            constraints.duration = parseInt(durationMatch[1]);
        }
        
        // Viewing preferences
        if (lowerText.includes('land') || lowerText.includes('shore')) {
            constraints.viewingType = 'land';
        }
        if (lowerText.includes('boat') || lowerText.includes('ferry')) {
            constraints.viewingType = 'boat';
        }
        if (lowerText.includes('balcony')) {
            constraints.accommodation = 'balcony';
        }
        
        // Location preferences
        if (lowerText.includes('san juan')) {
            constraints.region = 'san_juan_islands';
        }
        if (lowerText.includes('seattle')) {
            constraints.region = 'puget_sound';
        }
        
        return constraints;
    }

    /**
     * Generate multi-dimensional trip plan
     */
    async generateTripPlan(constraints) {
        const plan = {
            id: Date.now(),
            created: new Date().toISOString(),
            constraints: constraints,
            timeline: [],
            locations: [],
            logistics: {},
            alternatives: [],
            probabilityScore: 0
        };

        // Find optimal locations based on constraints
        const optimalLocations = this.findOptimalLocations(constraints);
        plan.locations = optimalLocations;

        // Generate timeline
        plan.timeline = this.generateTimeline(constraints, optimalLocations);

        // Add logistics
        plan.logistics = this.generateLogistics(constraints, optimalLocations);

        // Calculate overall probability score
        plan.probabilityScore = this.calculatePlanProbability(plan);

        // Generate alternatives
        plan.alternatives = this.generateAlternatives(plan);

        return plan;
    }

    /**
     * Find optimal viewing locations based on constraints
     */
    findOptimalLocations(constraints) {
        let locations = [...this.locations];

        // Filter by viewing type
        if (constraints.viewingType === 'land') {
            locations = locations.filter(loc => loc.landViewing);
        }

        // Filter by region
        if (constraints.region) {
            locations = locations.filter(loc => loc.region === constraints.region);
        }

        // Sort by probability and convenience
        locations.sort((a, b) => {
            const scoreA = this.calculateLocationScore(a, constraints);
            const scoreB = this.calculateLocationScore(b, constraints);
            return scoreB - scoreA;
        });

        // Return top locations based on duration
        const maxLocations = constraints.duration ? Math.min(constraints.duration * 2, 6) : 3;
        return locations.slice(0, maxLocations);
    }

    /**
     * Calculate location score based on constraints
     */
    calculateLocationScore(location, constraints) {
        let score = location.probabilityScore || 0.5;

        // Time preference bonus
        if (constraints.preferredTime && location.bestTimes?.includes(constraints.preferredTime)) {
            score += 0.2;
        }

        // Accessibility bonus
        if (constraints.accommodation === 'balcony' && location.balconyAccommodations) {
            score += 0.15;
        }

        // Weather reliability
        score += (location.weatherReliability || 0.5) * 0.1;

        return score;
    }

    /**
     * Generate day-by-day timeline
     */
    generateTimeline(constraints, locations) {
        const timeline = [];
        const duration = constraints.duration || 1;
        const preferredTime = constraints.preferredTime || 'morning';

        for (let day = 1; day <= duration; day++) {
            const dayPlan = {
                day: day,
                date: this.calculateDate(day),
                schedule: []
            };

            // Primary viewing location
            const location = locations[Math.min(day - 1, locations.length - 1)];
            
            if (preferredTime === 'morning' || preferredTime === 'all-day') {
                dayPlan.schedule.push({
                    time: '6:00 AM - 10:00 AM',
                    activity: 'Orca Watching',
                    location: location.name,
                    probabilityScore: location.probabilityScore,
                    details: 'Prime viewing hours with highest orca activity'
                });
            }

            if (preferredTime === 'afternoon' || preferredTime === 'all-day') {
                dayPlan.schedule.push({
                    time: '2:00 PM - 6:00 PM',
                    activity: 'Orca Watching',
                    location: location.name,
                    probabilityScore: location.probabilityScore * 0.8,
                    details: 'Afternoon viewing with good lighting'
                });
            }

            // Add meals and rest
            dayPlan.schedule.push({
                time: '12:00 PM - 1:00 PM',
                activity: 'Lunch',
                location: location.nearbyDining?.[0] || 'Local restaurant',
                details: 'Meal break with ocean view if available'
            });

            timeline.push(dayPlan);
        }

        return timeline;
    }

    /**
     * Generate logistics (accommodation, transportation, etc.)
     */
    generateLogistics(constraints, locations) {
        const logistics = {
            accommodation: [],
            transportation: [],
            dining: [],
            equipment: []
        };

        // Accommodation suggestions
        if (constraints.accommodation === 'balcony') {
            logistics.accommodation = locations
                .filter(loc => loc.balconyAccommodations)
                .map(loc => ({
                    name: loc.balconyAccommodations[0],
                    location: loc.name,
                    features: ['Ocean view balcony', 'Whale watching friendly'],
                    bookingUrl: '#'
                }));
        }

        // Transportation
        logistics.transportation.push({
            type: 'Car rental',
            recommendation: 'Recommended for flexibility between viewing locations',
            alternatives: ['Ferry system', 'Local shuttle services']
        });

        // Equipment recommendations
        logistics.equipment = [
            'Binoculars (8x42 recommended)',
            'Camera with telephoto lens',
            'Weather-appropriate clothing',
            'Snacks and water',
            'Portable chair (for land viewing)'
        ];

        return logistics;
    }

    /**
     * Calculate overall plan probability score
     */
    calculatePlanProbability(plan) {
        if (!plan.locations.length) return 0;

        const locationScores = plan.locations.map(loc => loc.probabilityScore || 0.5);
        const averageScore = locationScores.reduce((sum, score) => sum + score, 0) / locationScores.length;

        // Adjust for weather, season, and other factors
        const seasonAdjustment = this.getSeasonAdjustment();
        const weatherAdjustment = 0.9; // TODO: Get from weather API

        return Math.min(averageScore * seasonAdjustment * weatherAdjustment, 1.0);
    }

    /**
     * Display generated trip plan
     */
    displayTripPlan(plan) {
        this.currentPlan = plan;
        
        const planContainer = document.getElementById('trip-plan-display');
        if (!planContainer) return;

        planContainer.innerHTML = `
            <div class="trip-plan">
                <div class="plan-header">
                    <h3>Your Orca Watching Trip Plan</h3>
                    <div class="probability-score">
                        <span class="score">${(plan.probabilityScore * 100).toFixed(0)}%</span>
                        <span class="label">Success Probability</span>
                    </div>
                </div>
                
                <div class="plan-timeline">
                    ${plan.timeline.map(day => this.renderDayPlan(day)).join('')}
                </div>
                
                <div class="plan-logistics">
                    <h4>Logistics & Recommendations</h4>
                    ${this.renderLogistics(plan.logistics)}
                </div>
                
                <div class="plan-actions">
                    <button onclick="agenticPlanner.exportPlan('email')" class="btn-primary">
                        📧 Email Plan
                    </button>
                    <button onclick="agenticPlanner.exportPlan('calendar')" class="btn-secondary">
                        📅 Add to Calendar
                    </button>
                    <button onclick="agenticPlanner.sharePlan()" class="btn-secondary">
                        🔗 Share Plan
                    </button>
                </div>
            </div>
        `;
        
        planContainer.style.display = 'block';
    }

    /**
     * Render individual day plan
     */
    renderDayPlan(day) {
        return `
            <div class="day-plan">
                <h4>Day ${day.day} - ${new Date(day.date).toLocaleDateString()}</h4>
                <div class="schedule">
                    ${day.schedule.map(item => `
                        <div class="schedule-item">
                            <div class="time">${item.time}</div>
                            <div class="activity">
                                <strong>${item.activity}</strong>
                                <div class="location">${item.location}</div>
                                ${item.probabilityScore ? `
                                    <div class="probability">${(item.probabilityScore * 100).toFixed(0)}% chance</div>
                                ` : ''}
                                <div class="details">${item.details}</div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    /**
     * Export plan in various formats
     */
    async exportPlan(format) {
        if (!this.currentPlan) return;

        switch (format) {
            case 'email':
                this.exportToEmail();
                break;
            case 'calendar':
                this.exportToCalendar();
                break;
            case 'pdf':
                this.exportToPDF();
                break;
        }
    }

    /**
     * Export plan to email
     */
    exportToEmail() {
        const plan = this.currentPlan;
        const subject = `Your ORCAST Orca Watching Trip Plan`;
        const body = this.generateEmailContent(plan);
        
        const mailtoLink = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
        window.open(mailtoLink);
    }

    /**
     * Generate email content
     */
    generateEmailContent(plan) {
        return `
Your ORCAST Orca Watching Trip Plan
Success Probability: ${(plan.probabilityScore * 100).toFixed(0)}%

TIMELINE:
${plan.timeline.map(day => `
Day ${day.day} - ${new Date(day.date).toLocaleDateString()}
${day.schedule.map(item => `• ${item.time}: ${item.activity} at ${item.location}`).join('\n')}
`).join('\n')}

EQUIPMENT CHECKLIST:
${plan.logistics.equipment?.map(item => `☐ ${item}`).join('\n') || 'No equipment specified'}

CONTACTS & BOOKINGS:
• Accommodation: Contact details for reservations
• Transportation: Rental or ferry information
• Emergency: Local marine mammal rescue: (555) 123-4567

Generated by ORCAST - Optimizing your orca watching experience
Visit: https://orcast.org
        `.trim();
    }

    /**
     * Update voice UI status
     */
    updateVoiceUI(status, message = '') {
        const voiceButton = document.getElementById('voice-planning-btn');
        const voiceStatus = document.getElementById('voice-status');
        const voiceTranscript = document.getElementById('voice-transcript');

        if (voiceButton) {
            voiceButton.className = `voice-btn ${status}`;
            voiceButton.innerHTML = this.getVoiceButtonContent(status);
        }

        if (voiceStatus) {
            voiceStatus.textContent = this.getVoiceStatusText(status);
        }

        if (voiceTranscript && message) {
            voiceTranscript.textContent = message;
        }
    }

    /**
     * Get voice button content based on status
     */
    getVoiceButtonContent(status) {
        switch (status) {
            case 'listening': return '🎤 Listening...';
            case 'processing': return '🧠 Processing...';
            case 'error': return '❌ Error';
            default: return '🎤 Start Voice Planning';
        }
    }

    /**
     * Get helper methods
     */
    hasMinimumConstraints(constraints) {
        return Object.keys(constraints).length >= 2;
    }

    calculateDate(dayOffset) {
        const date = new Date();
        date.setDate(date.getDate() + dayOffset);
        return date.toISOString();
    }

    getSeasonAdjustment() {
        const month = new Date().getMonth();
        // Summer months have higher orca activity
        if (month >= 5 && month <= 8) return 1.0;
        if (month >= 3 && month <= 10) return 0.8;
        return 0.6;
    }

    extractViewingLocations() {
        // Extract unique viewing locations from orca sightings data
        // This would integrate with existing ORCAST data
        return [
            {
                name: 'Lime Kiln Point State Park',
                region: 'san_juan_islands',
                landViewing: true,
                probabilityScore: 0.85,
                bestTimes: ['morning', 'afternoon'],
                balconyAccommodations: ['Friday Harbor House', 'Earthbox Motel'],
                nearbyDining: ['Coho Restaurant', 'Market Chef'],
                weatherReliability: 0.9
            },
            {
                name: 'Deception Pass Bridge',
                region: 'puget_sound',
                landViewing: true,
                probabilityScore: 0.65,
                bestTimes: ['morning'],
                balconyAccommodations: ['Captain Whidbey Inn'],
                nearbyDining: ['Deception Pass Cafe'],
                weatherReliability: 0.8
            },
            {
                name: 'Mukilteo Lighthouse Park',
                region: 'puget_sound',
                landViewing: true,
                probabilityScore: 0.55,
                bestTimes: ['afternoon'],
                balconyAccommodations: ['Silver Cloud Hotel'],
                nearbyDining: ['Ivars Mukilteo Landing'],
                weatherReliability: 0.7
            }
        ];
    }

    // Additional helper methods would go here...
}

// Initialize global agentic planner
window.agenticPlanner = new AgenticTripPlanner(); 
 