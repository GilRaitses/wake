/**
 * AI Trip Planner Integration for ORCAST Firebase App
 * Provides voice/text input for trip constraints and generates event containers
 */

class AITripPlanner {
    constructor() {
        this.gemmaEndpoint = 'https://orcast-gemma3-gpu-126424997157.europe-west4.run.app/api/generate';
        this.authToken = null;
        this.isListening = false;
        this.recognition = null;
        this.events = [];
        this.secondAgent = new AnalyticsAgent();
        
        this.initializeVoiceRecognition();
        this.getAuthToken();
    }

    async getAuthToken() {
        try {
            const response = await fetch('/get-auth-token');
            const data = await response.json();
            this.authToken = data.token;
        } catch (error) {
            console.warn('Auth token not available:', error);
            // Fallback to direct gcloud call
            this.authToken = 'fallback';
        }
    }

    initializeVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onstart = () => {
                this.isListening = true;
                this.updateMicrophoneButton();
                this.showListeningIndicator();
            };
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                document.getElementById('ai-input-field').value = transcript;
                this.processConstraints(transcript);
            };
            
            this.recognition.onend = () => {
                this.isListening = false;
                this.updateMicrophoneButton();
                this.hideListeningIndicator();
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.isListening = false;
                this.updateMicrophoneButton();
                this.hideListeningIndicator();
            };
        }
    }

    createPlannerInterface() {
        return `
            <div class="ai-trip-planner" id="ai-trip-planner">
                <div class="planner-header">
                    <h3>🤖 AI Trip Planner</h3>
                    <button class="collapse-btn" onclick="aiPlanner.toggleCollapse()">−</button>
                </div>
                
                <div class="planner-content" id="planner-content">
                    <div class="input-section">
                        <div class="input-group">
                            <input 
                                type="text" 
                                id="ai-input-field" 
                                placeholder="Describe your trip constraints: 'I want to see orcas on August 13th from my suite at Rosario...'"
                                class="ai-input"
                            />
                            <button 
                                class="mic-btn" 
                                id="mic-btn" 
                                onclick="aiPlanner.toggleVoiceInput()"
                                title="Voice input"
                            >
                                🎤
                            </button>
                            <button 
                                class="submit-btn" 
                                onclick="aiPlanner.processInputConstraints()"
                            >
                                ✨ Generate Plan
                            </button>
                        </div>
                        
                        <div class="quick-prompts">
                            <span class="prompt-label">Quick prompts:</span>
                            <button class="quick-prompt" onclick="aiPlanner.useQuickPrompt('morning-kayak')">Morning Kayaking</button>
                            <button class="quick-prompt" onclick="aiPlanner.useQuickPrompt('evening-suite')">Evening from Suite</button>
                            <button class="quick-prompt" onclick="aiPlanner.useQuickPrompt('full-day')">Full Day Optimization</button>
                        </div>
                    </div>

                    <div class="listening-indicator" id="listening-indicator" style="display: none;">
                        <div class="pulse-dot"></div>
                        <span>Listening... Speak your trip constraints</span>
                    </div>

                    <div class="processing-status" id="processing-status" style="display: none;">
                        <div class="spinner"></div>
                        <span>AI analyzing constraints and generating optimized schedule...</span>
                    </div>

                    <div class="events-container" id="events-container">
                        <!-- Generated events will appear here -->
                    </div>
                </div>
            </div>
        `;
    }

    createPlannerStyles() {
        return `
            <style>
                .ai-trip-planner {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 12px;
                    margin: 15px;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                    color: white;
                    position: relative;
                    z-index: 1000;
                }

                .planner-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 15px 20px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 12px 12px 0 0;
                    backdrop-filter: blur(10px);
                }

                .planner-header h3 {
                    margin: 0;
                    font-size: 1.2em;
                    font-weight: 600;
                }

                .collapse-btn {
                    background: rgba(255,255,255,0.2);
                    border: none;
                    color: white;
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    cursor: pointer;
                    font-size: 1.2em;
                    transition: all 0.3s ease;
                }

                .collapse-btn:hover {
                    background: rgba(255,255,255,0.3);
                    transform: scale(1.1);
                }

                .planner-content {
                    padding: 20px;
                    transition: all 0.3s ease;
                }

                .planner-content.collapsed {
                    display: none;
                }

                .input-group {
                    display: flex;
                    gap: 10px;
                    margin-bottom: 15px;
                }

                .ai-input {
                    flex: 1;
                    padding: 12px 15px;
                    border: 2px solid rgba(255,255,255,0.3);
                    border-radius: 25px;
                    background: rgba(255,255,255,0.1);
                    color: white;
                    font-size: 0.95em;
                    backdrop-filter: blur(10px);
                }

                .ai-input::placeholder {
                    color: rgba(255,255,255,0.7);
                }

                .ai-input:focus {
                    outline: none;
                    border-color: rgba(255,255,255,0.6);
                    background: rgba(255,255,255,0.15);
                }

                .mic-btn, .submit-btn {
                    padding: 12px 18px;
                    border: none;
                    border-radius: 25px;
                    cursor: pointer;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    min-width: 50px;
                }

                .mic-btn {
                    background: rgba(255,255,255,0.2);
                    color: white;
                    font-size: 1.1em;
                }

                .mic-btn:hover {
                    background: rgba(255,255,255,0.3);
                    transform: scale(1.05);
                }

                .mic-btn.listening {
                    background: #e53e3e;
                    animation: pulse 1.5s infinite;
                }

                .submit-btn {
                    background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
                    color: white;
                }

                .submit-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                }

                .quick-prompts {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    flex-wrap: wrap;
                }

                .prompt-label {
                    font-size: 0.9em;
                    opacity: 0.8;
                    margin-right: 5px;
                }

                .quick-prompt {
                    background: rgba(255,255,255,0.15);
                    border: 1px solid rgba(255,255,255,0.3);
                    color: white;
                    padding: 6px 12px;
                    border-radius: 15px;
                    font-size: 0.85em;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }

                .quick-prompt:hover {
                    background: rgba(255,255,255,0.25);
                    transform: translateY(-1px);
                }

                .listening-indicator {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    padding: 15px;
                    background: rgba(229, 62, 62, 0.2);
                    border-radius: 8px;
                    margin: 15px 0;
                }

                .pulse-dot {
                    width: 12px;
                    height: 12px;
                    background: #e53e3e;
                    border-radius: 50%;
                    animation: pulse 1s infinite;
                }

                .processing-status {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    padding: 15px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 8px;
                    margin: 15px 0;
                }

                .spinner {
                    width: 16px;
                    height: 16px;
                    border: 2px solid rgba(255,255,255,0.3);
                    border-top: 2px solid white;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                }

                .events-container {
                    margin-top: 20px;
                }

                .event-item {
                    background: rgba(255,255,255,0.1);
                    border-radius: 8px;
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 4px solid #48bb78;
                    backdrop-filter: blur(10px);
                }

                .event-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 10px;
                }

                .event-title {
                    font-weight: 600;
                    font-size: 1.1em;
                }

                .event-probability {
                    background: #48bb78;
                    color: white;
                    padding: 4px 8px;
                    border-radius: 12px;
                    font-size: 0.9em;
                    font-weight: 600;
                }

                .event-details {
                    font-size: 0.95em;
                    opacity: 0.9;
                    line-height: 1.4;
                }

                .event-actions {
                    margin-top: 10px;
                    display: flex;
                    gap: 8px;
                }

                .event-btn {
                    background: rgba(255,255,255,0.2);
                    border: 1px solid rgba(255,255,255,0.3);
                    color: white;
                    padding: 6px 12px;
                    border-radius: 15px;
                    font-size: 0.85em;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }

                .event-btn:hover {
                    background: rgba(255,255,255,0.3);
                }

                @keyframes pulse {
                    0% { opacity: 1; transform: scale(1); }
                    50% { opacity: 0.5; transform: scale(1.1); }
                    100% { opacity: 1; transform: scale(1); }
                }

                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }

                /* Responsive */
                @media (max-width: 768px) {
                    .input-group {
                        flex-direction: column;
                    }
                    
                    .quick-prompts {
                        justify-content: center;
                    }
                }
                
                /* Structured Response Styles */
                .structured-response {
                    background: #f8fafc;
                    border-radius: 12px;
                    padding: 20px;
                    margin: 15px 0;
                }
                
                .forecast-overview {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                }
                
                .overview-text {
                    margin: 10px 0 0 0;
                    font-size: 1.1em;
                    line-height: 1.6;
                }
                
                .interactive-timeline {
                    background: white;
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                }
                
                .timeline-container {
                    display: flex;
                    gap: 10px;
                    overflow-x: auto;
                    padding: 10px 0;
                }
                
                .timeline-entry {
                    flex-shrink: 0;
                    width: 80px;
                    text-align: center;
                    padding: 10px;
                    border-radius: 8px;
                    border: 2px solid transparent;
                    transition: all 0.3s ease;
                }
                
                .timeline-entry.high {
                    background: #fee;
                    border-color: #ff4444;
                }
                
                .timeline-entry.medium {
                    background: #fff5e6;
                    border-color: #ffa500;
                }
                
                .timeline-entry.low {
                    background: #f0fff4;
                    border-color: #4caf50;
                }
                
                .timeline-time {
                    font-weight: bold;
                    font-size: 0.9em;
                    margin-bottom: 5px;
                }
                
                .timeline-probability {
                    font-size: 1.2em;
                    font-weight: bold;
                    margin-bottom: 5px;
                }
                
                .timeline-bar {
                    height: 40px;
                    background: #eee;
                    border-radius: 4px;
                    position: relative;
                    margin-bottom: 5px;
                }
                
                .timeline-fill {
                    background: currentColor;
                    border-radius: 4px;
                    width: 100%;
                    position: absolute;
                    bottom: 0;
                    transition: height 0.3s ease;
                }
                
                .timeline-summary {
                    font-size: 0.8em;
                    color: #666;
                }
                
                .map-config-preview {
                    background: white;
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                }
                
                .map-preview-info {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                }
                
                .action-buttons {
                    background: white;
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                }
                
                .actions-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 10px;
                }
                
                .action-btn {
                    background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
                    color: white;
                    border: none;
                    padding: 12px 16px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: 500;
                    transition: all 0.3s ease;
                }
                
                .action-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
                }
                
                .json-output-section {
                    background: white;
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                }
                
                .toggle-json-btn {
                    background: #666;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    cursor: pointer;
                    margin-bottom: 10px;
                }
                
                .json-output {
                    background: #f7fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 6px;
                    padding: 15px;
                    font-family: 'Courier New', monospace;
                    font-size: 0.9em;
                    max-height: 400px;
                    overflow-y: auto;
                }
            </style>
        `;
    }

    toggleVoiceInput() {
        if (!this.recognition) {
            alert('Voice recognition not supported in this browser');
            return;
        }

        if (this.isListening) {
            this.recognition.stop();
        } else {
            this.recognition.start();
        }
    }

    updateMicrophoneButton() {
        const micBtn = document.getElementById('mic-btn');
        if (this.isListening) {
            micBtn.classList.add('listening');
            micBtn.textContent = '🔴';
        } else {
            micBtn.classList.remove('listening');
            micBtn.textContent = '🎤';
        }
    }

    showListeningIndicator() {
        document.getElementById('listening-indicator').style.display = 'flex';
    }

    hideListeningIndicator() {
        document.getElementById('listening-indicator').style.display = 'none';
    }

    useQuickPrompt(type) {
        const prompts = {
            'morning-kayak': 'I want to go kayaking tomorrow morning from 7:30 AM to 12:00 PM for the best orca viewing opportunities',
            'evening-suite': 'I\'m staying at the Round House Suite at Rosario and want to watch for orcas from my room in the evening around 6-8 PM',
            'full-day': 'Optimize my full day on August 13th at Orcas Island for maximum orca encounter probability, staying at Rosario Village'
        };
        
        document.getElementById('ai-input-field').value = prompts[type];
    }

    async processInputConstraints() {
        const input = document.getElementById('ai-input-field').value.trim();
        if (!input) return;

        this.showProcessingStatus();
        
        try {
            // Extract constraints from user input
            const constraints = await this.extractConstraints(input);
            
            // Load the agentic response formatter
            const formatter = new AgenticResponseFormatter();
            
            // Generate structured response using the new schema
            const structuredResponse = await this.generateStructuredResponse(constraints, formatter);
            
            // Display the structured response in the UI
            this.displayStructuredResponse(structuredResponse);
            
            // Trigger second agent for analytics
            this.secondAgent.generateAnalyticsDashboard(structuredResponse);
            
            console.log('🎯 Generated structured agent response:', structuredResponse);
            
        } catch (error) {
            console.error('Error processing constraints:', error);
            this.showError(error.message);
        } finally {
            this.hideProcessingStatus();
        }
    }

    async processConstraints(transcript) {
        // Same as processInputConstraints but for voice input
        await this.processInputConstraints();
    }

    /**
     * Generate structured response using the agentic formatter
     */
    async generateStructuredResponse(constraints, formatter) {
        try {
            // Get current environmental data
            const environmentalData = await this.fetchEnvironmentalData();
            
            // Get forecast data
            const forecastData = await this.fetchForecastData();
            
            // Use the formatter to create the structured response
            const structuredResponse = await formatter.formatTripPlanResponse(
                constraints, 
                environmentalData, 
                forecastData
            );
            
            return structuredResponse;
            
        } catch (error) {
            console.error('Error generating structured response:', error);
            return formatter.getErrorResponse(error.message);
        }
    }

    /**
     * Fetch real environmental data from API
     */
    async fetchEnvironmentalData() {
        try {
            const response = await fetch('/api/real-time-data');
            const data = await response.json();
            return data.data;
        } catch (error) {
            console.warn('Could not fetch environmental data, using defaults:', error);
            return {
                tidalHeight: 2.3,
                seaTemperature: 16.1,
                salmonCount: 342,
                dataQuality: 'estimated'
            };
        }
    }

    /**
     * Fetch forecast data from API
     */
    async fetchForecastData() {
        try {
            const response = await fetch('/api/predictions');
            const data = await response.json();
            
            // Convert predictions data to expected format
            return {
                prediction_zones: data.data.zones || [],
                timestamp: data.timestamp,
                model_accuracy: data.data.modelAccuracy
            };
        } catch (error) {
            console.warn('Could not fetch forecast data, using defaults:', error);
            return {
                prediction_zones: [
                    { coordinates: [-123.0, 48.5], probability: 0.65, radius: 1000 },
                    { coordinates: [-123.2, 48.6], probability: 0.72, radius: 1500 }
                ],
                timestamp: new Date().toISOString(),
                model_accuracy: 0.89
            };
        }
    }

    /**
     * Display structured response in the UI
     */
    displayStructuredResponse(response) {
        const outputContainer = document.getElementById('ai-planner-output');
        
        // Create structured display
        const structuredHTML = `
            <div class="structured-response">
                <!-- Forecast Overview -->
                <div class="forecast-overview">
                    <h3>🔮 Forecast Overview</h3>
                    <p class="overview-text">${response.forecastOverview}</p>
                </div>
                
                <!-- Interactive Timeline -->
                <div class="interactive-timeline">
                    <h3>⏰ 24-Hour Probability Timeline</h3>
                    <div class="timeline-container">
                        ${this.generateTimelineHTML(response.timeSeries)}
                    </div>
                </div>
                
                <!-- Map Configuration Preview -->
                <div class="map-config-preview">
                    <h3>🗺️ Map Configuration</h3>
                    <div class="map-preview-info">
                        <div class="map-center">
                            <strong>Center:</strong> ${response.mapConfig.center.lat.toFixed(3)}, ${response.mapConfig.center.lng.toFixed(3)}
                        </div>
                        <div class="map-zoom">
                            <strong>Zoom Level:</strong> ${response.mapConfig.zoomLevel}
                        </div>
                        <div class="map-overlays">
                            <strong>Overlays:</strong> ${response.mapConfig.overlays.length} layers
                            <ul>
                                ${response.mapConfig.overlays.map(overlay => 
                                    `<li>${overlay.type.replace('_', ' ').toUpperCase()}</li>`
                                ).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Action Buttons -->
                <div class="action-buttons">
                    <h3>🎯 Available Actions</h3>
                    <div class="actions-grid">
                        ${response.actions.map(action => 
                            `<button class="action-btn" onclick="aiPlanner.executeAction('${action.type}', ${JSON.stringify(action.payload).replace(/"/g, '&quot;')})">
                                ${action.label}
                            </button>`
                        ).join('')}
                    </div>
                </div>
                
                <!-- Raw JSON Data (for debugging/integration) -->
                <div class="json-output-section">
                    <h3>📋 Schema-Compliant JSON Output</h3>
                    <button class="toggle-json-btn" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none'">
                        Toggle Raw JSON
                    </button>
                    <pre class="json-output" style="display: none;">${JSON.stringify(response, null, 2)}</pre>
                </div>
            </div>
        `;
        
        outputContainer.innerHTML = structuredHTML;
        
        // Store the response data for map integration
        this.lastStructuredResponse = response;
        
        // Emit event for map feature module to consume
        window.dispatchEvent(new CustomEvent('agentResponseGenerated', {
            detail: { response }
        }));
    }

    /**
     * Generate timeline HTML from timeSeries data
     */
    generateTimelineHTML(timeSeries) {
        return timeSeries.slice(0, 12).map((entry, index) => {
            const time = new Date(entry.timestamp);
            const hour = time.getHours();
            const probabilityPercent = (entry.probability * 100).toFixed(0);
            const probabilityClass = entry.probability > 0.7 ? 'high' : entry.probability > 0.4 ? 'medium' : 'low';
            
            return `
                <div class="timeline-entry ${probabilityClass}" title="${entry.summary}">
                    <div class="timeline-time">${hour}:00</div>
                    <div class="timeline-probability">${probabilityPercent}%</div>
                    <div class="timeline-bar">
                        <div class="timeline-fill" style="height: ${probabilityPercent}%"></div>
                    </div>
                    <div class="timeline-summary">${entry.summary.substring(0, 30)}...</div>
                </div>
            `;
        }).join('');
    }

    /**
     * Execute actions from the structured response
     */
    executeAction(actionType, payload) {
        console.log(`🎬 Executing action: ${actionType}`, payload);
        
        switch (actionType) {
            case 'save_plan':
                this.saveTripPlan(payload);
                break;
            case 'set_alert':
                this.setAlert(payload);
                break;
            case 'export_data':
                this.exportData(payload);
                break;
            case 'refresh_forecast':
                this.refreshForecast(payload);
                break;
            case 'retry':
                this.processInputConstraints(); // Retry the plan generation
                break;
            default:
                console.warn('Unknown action type:', actionType);
        }
    }

    /**
     * Save trip plan to local storage or Firebase
     */
    saveTripPlan(payload) {
        try {
            const tripPlans = JSON.parse(localStorage.getItem('orcaTripPlans') || '[]');
            tripPlans.push({
                id: Date.now(),
                ...payload.planData,
                saved_at: new Date().toISOString()
            });
            localStorage.setItem('orcaTripPlans', JSON.stringify(tripPlans));
            
            this.showNotification('Trip plan saved successfully!', 'success');
        } catch (error) {
            console.error('Error saving trip plan:', error);
            this.showNotification('Failed to save trip plan', 'error');
        }
    }

    /**
     * Set probability alert
     */
    setAlert(payload) {
        // Store alert preferences
        localStorage.setItem('orcaAlertSettings', JSON.stringify(payload));
        this.showNotification(`Alert set for ${payload.thresholds.probability * 100}% probability threshold`, 'success');
    }

    /**
     * Export forecast data
     */
    exportData(payload) {
        if (!this.lastStructuredResponse) return;
        
        const dataToExport = {
            forecast: this.lastStructuredResponse,
            exported_at: new Date().toISOString(),
            format: payload.formats[0] || 'json'
        };
        
        // Create downloadable file
        const blob = new Blob([JSON.stringify(dataToExport, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `orca_forecast_${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
        
        this.showNotification('Forecast data exported successfully!', 'success');
    }

    /**
     * Refresh forecast with latest data
     */
    async refreshForecast(payload) {
        this.showNotification('Refreshing forecast data...', 'info');
        
        try {
            // Re-generate the plan with fresh data
            await this.processInputConstraints();
            this.showNotification('Forecast updated with latest data!', 'success');
        } catch (error) {
            console.error('Error refreshing forecast:', error);
            this.showNotification('Failed to refresh forecast', 'error');
        }
    }

    /**
     * Show notification to user
     */
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        // Style the notification
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 6px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            opacity: 0;
            transition: opacity 0.3s ease;
            background: ${type === 'success' ? '#48bb78' : type === 'error' ? '#e53e3e' : '#4299e1'};
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Fade in
        setTimeout(() => notification.style.opacity = '1', 100);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    /**
     * Get map configuration for external integration
     */
    getMapConfigForIntegration() {
        return this.lastStructuredResponse?.mapConfig || null;
    }

    async extractConstraints(input) {
        const extractionPrompt = `
Extract trip planning constraints from this input: "${input}"

Return JSON format:
{
    "date": "YYYY-MM-DD or relative like 'tomorrow'",
    "timeWindows": [{"start": "HH:MM", "end": "HH:MM", "activity": "description"}],
    "location": "specific place or area",
    "accommodation": "where staying",
    "activities": ["list", "of", "desired", "activities"],
    "priorities": ["what's most important"],
    "constraints": ["any limitations or requirements"]
}

Be specific and extract all mentioned details.
        `;

        const response = await this.callGemma(extractionPrompt);
        try {
            return JSON.parse(response);
        } catch (e) {
            // Fallback parsing if JSON is malformed
            return this.parseConstraintsManually(input);
        }
    }

    async generateOptimizedPlan(constraints) {
        const optimizationPrompt = `
Create optimized trip plan using ORCAST real-time data and these constraints:
${JSON.stringify(constraints, null, 2)}

Current Conditions (use real Firebase data if available):
- Tidal height: 2.3ft rising
- Salmon count: 342 (high)
- Vessel noise: 125dB (moderate)
- Wave height: 1.2m (calm)

Return JSON format:
{
    "events": [
        {
            "id": "unique_id",
            "title": "Activity Name",
            "startTime": "HH:MM",
            "endTime": "HH:MM",
            "probability": 85,
            "location": "specific viewing zone",
            "description": "detailed description",
            "reasoning": "why this timing is optimal",
            "mapCenter": {"lat": 48.5, "lng": -123.0},
            "zoomLevel": 13,
            "environmentalFactors": ["tidal influence", "salmon activity", "weather"]
        }
    ],
    "overallProbability": 78,
    "confidence": "high",
    "alternatives": ["backup options"]
}

Provide 2-4 optimized time slots with specific reasoning.
        `;

        const response = await this.callGemma(optimizationPrompt);
        try {
            return JSON.parse(response);
        } catch (e) {
            console.error('Failed to parse optimization response:', response);
            return this.createFallbackPlan(constraints);
        }
    }

    async callGemma(prompt) {
        if (!this.authToken || this.authToken === 'fallback') {
            throw new Error('Authentication not available');
        }

        const response = await fetch(this.gemmaEndpoint, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: 'gemma3:4b',
                prompt: prompt,
                stream: false
            })
        });

        if (!response.ok) {
            throw new Error(`Gemma API error: ${response.status}`);
        }

        const data = await response.json();
        return data.response;
    }

    createEventContainers(plan) {
        const container = document.getElementById('events-container');
        container.innerHTML = '';

        if (!plan.events || plan.events.length === 0) {
            container.innerHTML = '<div class="no-events">No optimized events generated. Please try a different prompt.</div>';
            return;
        }

        plan.events.forEach(event => {
            const eventElement = this.createEventElement(event);
            container.appendChild(eventElement);
        });

        // Add overall summary
        const summary = document.createElement('div');
        summary.className = 'plan-summary';
        summary.innerHTML = `
            <h4>📊 Plan Summary</h4>
            <p><strong>Overall Probability:</strong> ${plan.overallProbability || 'N/A'}%</p>
            <p><strong>Confidence:</strong> ${plan.confidence || 'Medium'}</p>
            ${plan.alternatives ? `<p><strong>Alternatives:</strong> ${plan.alternatives.join(', ')}</p>` : ''}
        `;
        container.appendChild(summary);
    }

    createEventElement(event) {
        const eventDiv = document.createElement('div');
        eventDiv.className = 'event-item';
        eventDiv.innerHTML = `
            <div class="event-header">
                <div class="event-title">${event.title}</div>
                <div class="event-probability">${event.probability}%</div>
            </div>
            <div class="event-details">
                <p><strong>⏰ Time:</strong> ${event.startTime} - ${event.endTime}</p>
                <p><strong>📍 Location:</strong> ${event.location}</p>
                <p><strong>📝 Description:</strong> ${event.description}</p>
                <p><strong>🧠 AI Reasoning:</strong> ${event.reasoning}</p>
                ${event.environmentalFactors ? `<p><strong>🌊 Factors:</strong> ${event.environmentalFactors.join(', ')}</p>` : ''}
            </div>
            <div class="event-actions">
                <button class="event-btn" onclick="aiPlanner.previewOnMap('${event.id}')">🗺️ Preview Map</button>
                <button class="event-btn" onclick="aiPlanner.showAnalytics('${event.id}')">📊 Analytics</button>
                <button class="event-btn" onclick="aiPlanner.addToCalendar('${event.id}')">📅 Add to Calendar</button>
            </div>
        `;
        
        // Store event data for later use
        eventDiv.dataset.eventData = JSON.stringify(event);
        
        return eventDiv;
    }

    previewOnMap(eventId) {
        const eventElement = document.querySelector(`[data-event-data*='"id":"${eventId}"']`);
        if (!eventElement) return;
        
        const eventData = JSON.parse(eventElement.dataset.eventData);
        
        // Focus map on event location
        if (window.map && eventData.mapCenter) {
            window.map.setCenter(eventData.mapCenter);
            window.map.setZoom(eventData.zoomLevel || 13);
            
            // Add temporary marker
            this.addEventMarker(eventData);
        }
        
        // Trigger second agent for detailed preview
        this.secondAgent.generateMapPreview(eventData);
    }

    showAnalytics(eventId) {
        const eventElement = document.querySelector(`[data-event-data*='"id":"${eventId}"']`);
        if (!eventElement) return;
        
        const eventData = JSON.parse(eventElement.dataset.eventData);
        this.secondAgent.showEventAnalytics(eventData);
    }

    addToCalendar(eventId) {
        const eventElement = document.querySelector(`[data-event-data*='"id":"${eventId}"']`);
        if (!eventElement) return;
        
        const eventData = JSON.parse(eventElement.dataset.eventData);
        
        // Create calendar event
        const startDate = new Date();
        startDate.setHours(parseInt(eventData.startTime.split(':')[0]), parseInt(eventData.startTime.split(':')[1]));
        
        const endDate = new Date();
        endDate.setHours(parseInt(eventData.endTime.split(':')[0]), parseInt(eventData.endTime.split(':')[1]));
        
        const calendarUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${encodeURIComponent(eventData.title)}&dates=${startDate.toISOString().replace(/[-:]/g, '').split('.')[0]}Z/${endDate.toISOString().replace(/[-:]/g, '').split('.')[0]}Z&details=${encodeURIComponent(eventData.description)}&location=${encodeURIComponent(eventData.location)}`;
        
        window.open(calendarUrl, '_blank');
    }

    addEventMarker(eventData) {
        if (!window.map) return;
        
        // Remove existing temporary markers
        if (window.tempMarkers) {
            window.tempMarkers.forEach(marker => marker.setMap(null));
        }
        window.tempMarkers = [];
        
        const marker = new google.maps.Marker({
            position: eventData.mapCenter,
            map: window.map,
            title: eventData.title,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 10,
                fillColor: '#48bb78',
                fillOpacity: 0.8,
                strokeColor: '#ffffff',
                strokeWeight: 2
            }
        });
        
        const infoWindow = new google.maps.InfoWindow({
            content: `
                <div style="color: black;">
                    <h4>${eventData.title}</h4>
                    <p><strong>Time:</strong> ${eventData.startTime} - ${eventData.endTime}</p>
                    <p><strong>Probability:</strong> ${eventData.probability}%</p>
                    <p>${eventData.description}</p>
                </div>
            `
        });
        
        marker.addListener('click', () => {
            infoWindow.open(window.map, marker);
        });
        
        window.tempMarkers.push(marker);
        
        // Auto-open info window
        setTimeout(() => infoWindow.open(window.map, marker), 500);
    }

    toggleCollapse() {
        const content = document.getElementById('planner-content');
        const button = document.querySelector('.collapse-btn');
        
        if (content.classList.contains('collapsed')) {
            content.classList.remove('collapsed');
            button.textContent = '−';
        } else {
            content.classList.add('collapsed');
            button.textContent = '+';
        }
    }

    showProcessingStatus() {
        document.getElementById('processing-status').style.display = 'flex';
        document.getElementById('events-container').innerHTML = '';
    }

    hideProcessingStatus() {
        document.getElementById('processing-status').style.display = 'none';
    }

    showError(message) {
        const container = document.getElementById('events-container');
        container.innerHTML = `<div class="error-message" style="color: #e53e3e; padding: 15px; text-align: center;">❌ Error: ${message}</div>`;
    }

    parseConstraintsManually(input) {
        // Fallback manual parsing
        return {
            date: 'today',
            timeWindows: [{ start: '08:00', end: '18:00', activity: 'orca viewing' }],
            location: 'San Juan Islands',
            accommodation: 'unknown',
            activities: ['orca watching'],
            priorities: ['wildlife viewing'],
            constraints: []
        };
    }

    createFallbackPlan(constraints) {
        return {
            events: [
                {
                    id: 'fallback_1',
                    title: 'Morning Orca Viewing',
                    startTime: '08:00',
                    endTime: '12:00',
                    probability: 75,
                    location: 'San Juan Islands',
                    description: 'Optimal morning viewing based on typical patterns',
                    reasoning: 'Morning hours typically show higher orca activity',
                    mapCenter: { lat: 48.5, lng: -123.0 },
                    zoomLevel: 12,
                    environmentalFactors: ['tidal patterns', 'salmon activity']
                }
            ],
            overallProbability: 75,
            confidence: 'medium',
            alternatives: ['Evening viewing session']
        };
    }
}

/**
 * Second Agent: Analytics and Dashboard Generation
 */
class AnalyticsAgent {
    constructor() {
        this.dashboards = new Map();
    }

    async generateAnalyticsDashboard(plan) {
        console.log('🔬 Analytics Agent: Generating dashboard for plan', plan);
        
        // This would integrate with BigQuery for historical analysis
        const analyticsData = await this.fetchHistoricalAnalytics(plan);
        
        // Create dashboard widget
        this.createDashboardWidget(analyticsData);
    }

    async generateMapPreview(eventData) {
        console.log('🗺️ Analytics Agent: Generating map preview for', eventData);
        
        // Configure specialized map layers for this event
        this.configureEventMapLayers(eventData);
    }

    async showEventAnalytics(eventData) {
        console.log('📊 Analytics Agent: Showing analytics for', eventData);
        
        // Create analytics popup
        this.createAnalyticsPopup(eventData);
    }

    async fetchHistoricalAnalytics(plan) {
        // This would connect to BigQuery for historical data analysis
        return {
            historicalProbability: 0.82,
            seasonalTrends: 'increasing',
            weatherCorrelation: 0.76,
            timeOfDayOptimal: '08:00-10:00',
            moonPhaseInfluence: 'moderate'
        };
    }

    createDashboardWidget(data) {
        // Create floating analytics dashboard
        const widget = document.createElement('div');
        widget.className = 'analytics-widget';
        widget.innerHTML = `
            <div class="widget-header">
                <h4>📊 Trip Analytics</h4>
                <button onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
            <div class="widget-content">
                <div class="metric">
                    <span class="metric-label">Historical Success Rate:</span>
                    <span class="metric-value">${(data.historicalProbability * 100).toFixed(0)}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Seasonal Trend:</span>
                    <span class="metric-value">${data.seasonalTrends}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Weather Correlation:</span>
                    <span class="metric-value">${(data.weatherCorrelation * 100).toFixed(0)}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Optimal Time:</span>
                    <span class="metric-value">${data.timeOfDayOptimal}</span>
                </div>
            </div>
        `;
        
        // Add styles for widget
        if (!document.getElementById('analytics-widget-styles')) {
            const styles = document.createElement('style');
            styles.id = 'analytics-widget-styles';
            styles.textContent = `
                .analytics-widget {
                    position: fixed;
                    top: 100px;
                    right: 20px;
                    width: 300px;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    z-index: 2000;
                    animation: slideIn 0.3s ease-out;
                }
                
                .widget-header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px;
                    border-radius: 12px 12px 0 0;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .widget-content {
                    padding: 15px;
                }
                
                .metric {
                    display: flex;
                    justify-content: space-between;
                    margin: 10px 0;
                    padding: 8px;
                    background: #f7fafc;
                    border-radius: 6px;
                }
                
                .metric-label {
                    color: #4a5568;
                    font-size: 0.9em;
                }
                
                .metric-value {
                    font-weight: 600;
                    color: #2d3748;
                }
                
                @keyframes slideIn {
                    from { transform: translateX(100%); }
                    to { transform: translateX(0); }
                }
            `;
            document.head.appendChild(styles);
        }
        
        document.body.appendChild(widget);
        
        // Auto-remove after 10 seconds
        setTimeout(() => {
            if (widget.parentElement) {
                widget.remove();
            }
        }, 10000);
    }

    configureEventMapLayers(eventData) {
        // This would configure specific map layers for the event
        console.log('Configuring map layers for event:', eventData.title);
        
        // Add probability heat layer, current data, etc.
        // Integration with the main map instance
    }

    createAnalyticsPopup(eventData) {
        // Create detailed analytics popup
        const popup = document.createElement('div');
        popup.className = 'analytics-popup';
        popup.innerHTML = `
            <div class="popup-backdrop" onclick="this.parentElement.remove()"></div>
            <div class="popup-content">
                <div class="popup-header">
                    <h3>📊 Event Analytics: ${eventData.title}</h3>
                    <button onclick="this.parentElement.parentElement.remove()">×</button>
                </div>
                <div class="popup-body">
                    <div class="chart-placeholder">
                        <p>📈 Probability chart would appear here</p>
                        <p>🌊 Environmental factor analysis</p>
                        <p>📊 Historical comparison data</p>
                        <p>🎯 Real-time optimization suggestions</p>
                    </div>
                </div>
            </div>
        `;
        
        // Add popup styles
        if (!document.getElementById('popup-styles')) {
            const styles = document.createElement('style');
            styles.id = 'popup-styles';
            styles.textContent = `
                .analytics-popup {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: 3000;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                
                .popup-backdrop {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0,0,0,0.5);
                    backdrop-filter: blur(5px);
                }
                
                .popup-content {
                    background: white;
                    border-radius: 12px;
                    width: 90%;
                    max-width: 600px;
                    max-height: 80%;
                    overflow-y: auto;
                    position: relative;
                    animation: popupAppear 0.3s ease-out;
                }
                
                .popup-header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 12px 12px 0 0;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .popup-body {
                    padding: 20px;
                }
                
                .chart-placeholder {
                    background: #f7fafc;
                    border: 2px dashed #cbd5e0;
                    border-radius: 8px;
                    padding: 40px;
                    text-align: center;
                    color: #4a5568;
                }
                
                @keyframes popupAppear {
                    from { transform: scale(0.8); opacity: 0; }
                    to { transform: scale(1); opacity: 1; }
                }
            `;
            document.head.appendChild(styles);
        }
        
        document.body.appendChild(popup);
    }
}

// Initialize global AI planner
let aiPlanner;

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        aiPlanner = new AITripPlanner();
    });
} else {
    aiPlanner = new AITripPlanner();
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AITripPlanner, AnalyticsAgent };
} 