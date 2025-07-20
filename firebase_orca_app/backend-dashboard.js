/**
 * Backend API Dashboard - Preloaded Data Summaries
 * Automatically fetches and displays live data from all endpoints
 */

class BackendDashboard {
    constructor() {
        this.endpoints = {
            predictions: '/api/predictions',
            dtagData: '/api/dtag-data',
            realTimeData: '/api/real-time-data',
            feedingZones: '/api/feeding-zones',
            behavioralAnalysis: '/api/behavioral-analysis'
        };
        
        this.dashboardData = {};
        this.updateInterval = 30000; // 30 seconds
        this.intervals = [];
        
        this.initializeDashboard();
    }

    initializeDashboard() {
        console.log('🔄 Initializing Backend Dashboard...');
        
        // Create dashboard UI
        this.createDashboardUI();
        
        // Load all data initially
        this.loadAllEndpoints();
        
        // Set up auto-refresh intervals
        this.setupAutoRefresh();
        
        console.log('✅ Backend Dashboard initialized');
    }

    createDashboardUI() {
        return `
            <div class="backend-dashboard">
                <div class="dashboard-header">
                    <h2>🔍 Backend API Inspection Dashboard</h2>
                    <div class="dashboard-controls">
                        <span class="last-updated" id="dashboard-last-updated">Loading...</span>
                        <button class="refresh-btn" onclick="backendDashboard.refreshAll()">🔄 Refresh All</button>
                        <button class="settings-btn" onclick="backendDashboard.toggleSettings()">⚙️</button>
                    </div>
                </div>

                <div class="dashboard-grid">
                    <!-- Behavioral Predictions Summary -->
                    <div class="dashboard-card" id="predictions-card">
                        <div class="card-header">
                            <h3>🎯 Behavioral Predictions</h3>
                            <div class="status-indicator" id="predictions-status">⏳</div>
                        </div>
                        <div class="card-content" id="predictions-content">
                            <div class="loading-skeleton"></div>
                        </div>
                        <div class="card-footer">
                            <span class="endpoint-url">GET /api/predictions</span>
                            <button onclick="backendDashboard.viewDetails('predictions')">View Full Data</button>
                        </div>
                    </div>

                    <!-- DTAG Data Summary -->
                    <div class="dashboard-card" id="dtag-card">
                        <div class="card-header">
                            <h3>📡 DTAG Data Analysis</h3>
                            <div class="status-indicator" id="dtag-status">⏳</div>
                        </div>
                        <div class="card-content" id="dtag-content">
                            <div class="loading-skeleton"></div>
                        </div>
                        <div class="card-footer">
                            <span class="endpoint-url">GET /api/dtag-data</span>
                            <button onclick="backendDashboard.viewDetails('dtagData')">View Full Data</button>
                        </div>
                    </div>

                    <!-- Real-time Environmental Data -->
                    <div class="dashboard-card" id="realtime-card">
                        <div class="card-header">
                            <h3>🌊 Real-time Environmental</h3>
                            <div class="status-indicator" id="realtime-status">⏳</div>
                        </div>
                        <div class="card-content" id="realtime-content">
                            <div class="loading-skeleton"></div>
                        </div>
                        <div class="card-footer">
                            <span class="endpoint-url">GET /api/real-time-data</span>
                            <button onclick="backendDashboard.viewDetails('realTimeData')">View Full Data</button>
                        </div>
                    </div>

                    <!-- Feeding Zone Analytics -->
                    <div class="dashboard-card" id="feeding-card">
                        <div class="card-header">
                            <h3>🐟 Feeding Zone Analytics</h3>
                            <div class="status-indicator" id="feeding-status">⏳</div>
                        </div>
                        <div class="card-content" id="feeding-content">
                            <div class="loading-skeleton"></div>
                        </div>
                        <div class="card-footer">
                            <span class="endpoint-url">GET /api/feeding-zones</span>
                            <button onclick="backendDashboard.viewDetails('feedingZones')">View Full Data</button>
                        </div>
                    </div>

                    <!-- Behavioral ML Classification -->
                    <div class="dashboard-card" id="behavioral-card">
                        <div class="card-header">
                            <h3>🤖 ML Classification</h3>
                            <div class="status-indicator" id="behavioral-status">⏳</div>
                        </div>
                        <div class="card-content" id="behavioral-content">
                            <div class="loading-skeleton"></div>
                        </div>
                        <div class="card-footer">
                            <span class="endpoint-url">GET /api/behavioral-analysis</span>
                            <button onclick="backendDashboard.viewDetails('behavioralAnalysis')">View Full Data</button>
                        </div>
                    </div>

                    <!-- System Overview -->
                    <div class="dashboard-card system-overview">
                        <div class="card-header">
                            <h3>⚡ System Overview</h3>
                            <div class="status-indicator" id="system-status">⏳</div>
                        </div>
                        <div class="card-content" id="system-content">
                            <div class="system-metrics">
                                <div class="metric">
                                    <span class="metric-label">Active Endpoints:</span>
                                    <span class="metric-value" id="active-endpoints">-</span>
                                </div>
                                <div class="metric">
                                    <span class="metric-label">Avg Response Time:</span>
                                    <span class="metric-value" id="avg-response-time">-</span>
                                </div>
                                <div class="metric">
                                    <span class="metric-label">Data Freshness:</span>
                                    <span class="metric-value" id="data-freshness">-</span>
                                </div>
                                <div class="metric">
                                    <span class="metric-label">Error Rate:</span>
                                    <span class="metric-value" id="error-rate">-</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Detailed View Modal -->
                <div class="details-modal" id="details-modal" style="display: none;">
                    <div class="modal-backdrop" onclick="backendDashboard.closeDetails()"></div>
                    <div class="modal-content">
                        <div class="modal-header">
                            <h3 id="modal-title">Endpoint Details</h3>
                            <button onclick="backendDashboard.closeDetails()">×</button>
                        </div>
                        <div class="modal-body" id="modal-body">
                            <!-- Detailed data will be loaded here -->
                        </div>
                    </div>
                </div>

                <!-- Settings Panel -->
                <div class="settings-panel" id="settings-panel" style="display: none;">
                    <div class="settings-header">
                        <h4>Dashboard Settings</h4>
                        <button onclick="backendDashboard.toggleSettings()">×</button>
                    </div>
                    <div class="settings-content">
                        <div class="setting-item">
                            <label>Refresh Interval:</label>
                            <select onchange="backendDashboard.updateRefreshInterval(this.value)">
                                <option value="10000">10 seconds</option>
                                <option value="30000" selected>30 seconds</option>
                                <option value="60000">1 minute</option>
                                <option value="300000">5 minutes</option>
                            </select>
                        </div>
                        <div class="setting-item">
                            <label>Auto-refresh:</label>
                            <input type="checkbox" checked onchange="backendDashboard.toggleAutoRefresh(this.checked)">
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    createDashboardStyles() {
        return `
            <style>
                .backend-dashboard {
                    background: #f8fafc;
                    border-radius: 12px;
                    padding: 20px;
                    margin: 15px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                }

                .dashboard-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 25px;
                    padding-bottom: 15px;
                    border-bottom: 2px solid #e2e8f0;
                }

                .dashboard-header h2 {
                    margin: 0;
                    color: #2d3748;
                    font-size: 1.5em;
                }

                .dashboard-controls {
                    display: flex;
                    align-items: center;
                    gap: 15px;
                }

                .last-updated {
                    font-size: 0.9em;
                    color: #718096;
                }

                .refresh-btn, .settings-btn {
                    background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 0.9em;
                    transition: all 0.3s ease;
                }

                .refresh-btn:hover, .settings-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
                }

                .dashboard-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                    gap: 20px;
                }

                .dashboard-card {
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                    transition: all 0.3s ease;
                    border: 1px solid #e2e8f0;
                }

                .dashboard-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                }

                .card-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 15px 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-radius: 10px 10px 0 0;
                }

                .card-header h3 {
                    margin: 0;
                    font-size: 1.1em;
                    font-weight: 600;
                }

                .status-indicator {
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 0.8em;
                }

                .status-indicator.success {
                    background: #48bb78;
                    color: white;
                }

                .status-indicator.error {
                    background: #e53e3e;
                    color: white;
                }

                .status-indicator.loading {
                    background: #ed8936;
                    color: white;
                    animation: pulse 1.5s infinite;
                }

                .card-content {
                    padding: 20px;
                    min-height: 120px;
                }

                .card-footer {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 15px 20px;
                    background: #f7fafc;
                    border-radius: 0 0 10px 10px;
                    border-top: 1px solid #e2e8f0;
                }

                .endpoint-url {
                    font-family: 'Courier New', monospace;
                    font-size: 0.85em;
                    color: #4a5568;
                    background: #edf2f7;
                    padding: 4px 8px;
                    border-radius: 4px;
                }

                .card-footer button {
                    background: #4299e1;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 0.85em;
                    transition: all 0.3s ease;
                }

                .card-footer button:hover {
                    background: #3182ce;
                    transform: translateY(-1px);
                }

                .loading-skeleton {
                    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
                    background-size: 200% 100%;
                    animation: loading 1.5s infinite;
                    height: 80px;
                    border-radius: 6px;
                }

                .data-summary {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                }

                .summary-item {
                    text-align: center;
                    padding: 10px;
                    background: #f7fafc;
                    border-radius: 6px;
                }

                .summary-value {
                    font-size: 1.5em;
                    font-weight: bold;
                    color: #2d3748;
                    display: block;
                }

                .summary-label {
                    font-size: 0.85em;
                    color: #718096;
                    margin-top: 4px;
                }

                .system-overview {
                    grid-column: 1 / -1;
                }

                .system-metrics {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 15px;
                }

                .metric {
                    text-align: center;
                    padding: 15px;
                    background: #f7fafc;
                    border-radius: 8px;
                }

                .metric-value {
                    display: block;
                    font-size: 1.4em;
                    font-weight: bold;
                    color: #2d3748;
                    margin-bottom: 5px;
                }

                .metric-label {
                    font-size: 0.9em;
                    color: #718096;
                }

                .details-modal {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: 1000;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }

                .modal-backdrop {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0,0,0,0.5);
                    backdrop-filter: blur(5px);
                }

                .modal-content {
                    background: white;
                    border-radius: 12px;
                    width: 90%;
                    max-width: 800px;
                    max-height: 80%;
                    overflow-y: auto;
                    position: relative;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                }

                .modal-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-radius: 12px 12px 0 0;
                }

                .modal-body {
                    padding: 20px;
                    max-height: 500px;
                    overflow-y: auto;
                }

                .settings-panel {
                    position: fixed;
                    top: 100px;
                    right: 20px;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    z-index: 1500;
                    min-width: 250px;
                }

                .settings-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 15px;
                    background: #4299e1;
                    color: white;
                    border-radius: 10px 10px 0 0;
                }

                .settings-content {
                    padding: 15px;
                }

                .setting-item {
                    margin-bottom: 15px;
                }

                .setting-item label {
                    display: block;
                    margin-bottom: 5px;
                    font-weight: 500;
                    color: #2d3748;
                }

                .setting-item select {
                    width: 100%;
                    padding: 8px;
                    border: 1px solid #e2e8f0;
                    border-radius: 6px;
                }

                @keyframes loading {
                    0% { background-position: 200% 0; }
                    100% { background-position: -200% 0; }
                }

                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }

                /* Responsive */
                @media (max-width: 768px) {
                    .dashboard-grid {
                        grid-template-columns: 1fr;
                    }
                    
                    .data-summary {
                        grid-template-columns: 1fr;
                    }
                    
                    .system-metrics {
                        grid-template-columns: repeat(2, 1fr);
                    }
                }
            </style>
        `;
    }

    async loadAllEndpoints() {
        const startTime = Date.now();
        const promises = [];
        
        // Load all endpoints in parallel
        for (const [key, endpoint] of Object.entries(this.endpoints)) {
            promises.push(this.loadEndpointData(key, endpoint));
        }
        
        // Wait for all to complete
        const results = await Promise.allSettled(promises);
        
        // Update system overview
        this.updateSystemOverview(results, Date.now() - startTime);
        
        // Update last updated timestamp
        document.getElementById('dashboard-last-updated').textContent = 
            `Last updated: ${new Date().toLocaleTimeString()}`;
    }

    async loadEndpointData(key, endpoint) {
        const startTime = Date.now();
        
        try {
            // Update status to loading
            this.updateStatus(key, 'loading');
            
            // Connect to real API endpoints from the Firebase app
            const data = await this.fetchEndpointData(endpoint);
            const responseTime = Date.now() - startTime;
            
            // Store data
            this.dashboardData[key] = {
                data: data,
                responseTime: responseTime,
                lastUpdated: new Date(),
                status: 'success'
            };
            
            // Update UI
            this.updateCardContent(key, data);
            this.updateStatus(key, 'success');
            
            return { status: 'success', responseTime };
            
        } catch (error) {
            console.error(`Error loading ${endpoint}:`, error);
            
            this.dashboardData[key] = {
                error: error.message,
                lastUpdated: new Date(),
                status: 'error'
            };
            
            this.updateCardContent(key, null, error.message);
            this.updateStatus(key, 'error');
            
            return { status: 'error', error: error.message };
        }
    }

    async fetchEndpointData(endpoint) {
        // Connect to real API endpoints from the Firebase app
        try {
            const response = await fetch(endpoint, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            if (data.status === 'error') {
                throw new Error(data.message);
            }
            
            return data.data; // Return the data portion of the API response
            
        } catch (error) {
            console.error(`Error fetching ${endpoint}:`, error);
            throw error;
        }
    }

    // Remove all the simulate* methods and replace with real API calls
    // The fetchEndpointData method above now handles all real API calls

    updateCardContent(key, data, error = null) {
        const contentEl = document.getElementById(`${key.replace('Data', '').replace('Analysis', '')}-content`);
        
        if (error) {
            contentEl.innerHTML = `
                <div class="error-message" style="color: #e53e3e; text-align: center; padding: 20px;">
                    <div style="font-size: 1.2em; margin-bottom: 10px;">⚠️ Error</div>
                    <div style="font-size: 0.9em;">${error}</div>
                </div>
            `;
            return;
        }

        switch (key) {
            case 'predictions':
                contentEl.innerHTML = `
                    <div class="data-summary">
                        <div class="summary-item">
                            <span class="summary-value">${data.totalZones}</span>
                            <div class="summary-label">Total Zones</div>
                        </div>
                        <div class="summary-item">
                            <span class="summary-value">${data.activeZones}</span>
                            <div class="summary-label">Active Zones</div>
                        </div>
                        <div class="summary-item">
                            <span class="summary-value">${(data.avgProbability * 100).toFixed(0)}%</span>
                            <div class="summary-label">Avg Probability</div>
                        </div>
                        <div class="summary-item">
                            <span class="summary-value">${(data.modelAccuracy * 100).toFixed(0)}%</span>
                            <div class="summary-label">Model Accuracy</div>
                        </div>
                    </div>
                `;
                break;
                
            case 'dtagData':
                contentEl.innerHTML = `
                    <div class="data-summary">
                        <div class="summary-item">
                            <span class="summary-value">${data.activeTags}</span>
                            <div class="summary-label">Active Tags</div>
                        </div>
                        <div class="summary-item">
                            <span class="summary-value">${data.dataPoints.toLocaleString()}</span>
                            <div class="summary-label">Data Points</div>
                        </div>
                        <div class="summary-item">
                            <span class="summary-value">${data.avgDiveDepth}m</span>
                            <div class="summary-label">Avg Dive Depth</div>
                        </div>
                        <div class="summary-item">
                            <span class="summary-value">${data.forragingEvents}</span>
                            <div class="summary-label">Foraging Events</div>
                        </div>
                    </div>
                `;
                break;
                
            case 'realTimeData':
                contentEl.innerHTML = `
                    <div class="data-summary">
                        <div class="summary-item">
                            <span class="summary-value">${data.tidalHeight}ft</span>
                            <div class="summary-label">Tidal Height</div>
                        </div>
                        <div class="summary-item">
                            <span class="summary-value">${data.salmonCount}</span>
                            <div class="summary-label">Salmon Count</div>
                        </div>
                        <div class="summary-item">
                            <span class="summary-value">${data.seaTemperature}°C</span>
                            <div class="summary-label">Sea Temperature</div>
                        </div>
                        <div class="summary-item">
                            <span class="summary-value">${data.vesselNoise}dB</span>
                            <div class="summary-label">Vessel Noise</div>
                        </div>
                    </div>
                `;
                break;
                
            case 'feedingZones':
                contentEl.innerHTML = `
                    <div class="data-summary">
                        <div class="summary-item">
                            <span class="summary-value">${data.activeZones}</span>
                            <div class="summary-label">Active Zones</div>
                        </div>
                        <div class="summary-item">
                            <span class="summary-value">${data.totalFeedingEvents}</span>
                            <div class="summary-label">Feeding Events</div>
                        </div>
                        <div class="summary-item">
                            <span class="summary-value">${data.avgIntensity}/10</span>
                            <div class="summary-label">Avg Intensity</div>
                        </div>
                        <div class="summary-item">
                            <span class="summary-value">${(data.efficiency * 100).toFixed(0)}%</span>
                            <div class="summary-label">Efficiency</div>
                        </div>
                    </div>
                `;
                break;
                
            case 'behavioralAnalysis':
                contentEl.innerHTML = `
                    <div class="data-summary">
                        <div class="summary-item">
                            <span class="summary-value">${data.totalClassifications}</span>
                            <div class="summary-label">Classifications</div>
                        </div>
                        <div class="summary-item">
                            <span class="summary-value">${data.behaviors.foraging}</span>
                            <div class="summary-label">Foraging</div>
                        </div>
                        <div class="summary-item">
                            <span class="summary-value">${(data.modelConfidence * 100).toFixed(0)}%</span>
                            <div class="summary-label">Confidence</div>
                        </div>
                        <div class="summary-item">
                            <span class="summary-value">${data.processingTime}ms</span>
                            <div class="summary-label">Processing Time</div>
                        </div>
                    </div>
                `;
                break;
        }
    }

    updateStatus(key, status) {
        const statusEl = document.getElementById(`${key.replace('Data', '').replace('Analysis', '')}-status`);
        statusEl.className = `status-indicator ${status}`;
        
        switch (status) {
            case 'success':
                statusEl.textContent = '✅';
                break;
            case 'error':
                statusEl.textContent = '❌';
                break;
            case 'loading':
                statusEl.textContent = '⏳';
                break;
        }
    }

    updateSystemOverview(results, totalTime) {
        const successCount = results.filter(r => r.value?.status === 'success').length;
        const avgResponseTime = results
            .filter(r => r.value?.responseTime)
            .reduce((sum, r) => sum + r.value.responseTime, 0) / results.length;
        
        const errorRate = ((results.length - successCount) / results.length * 100).toFixed(1);
        
        document.getElementById('active-endpoints').textContent = `${successCount}/${results.length}`;
        document.getElementById('avg-response-time').textContent = `${Math.round(avgResponseTime)}ms`;
        document.getElementById('data-freshness').textContent = 'Live';
        document.getElementById('error-rate').textContent = `${errorRate}%`;
        
        // Update system status
        const systemStatus = successCount === results.length ? 'success' : 
                           successCount > results.length / 2 ? 'warning' : 'error';
        document.getElementById('system-status').className = `status-indicator ${systemStatus}`;
        document.getElementById('system-status').textContent = 
            systemStatus === 'success' ? '✅' : systemStatus === 'warning' ? '⚠️' : '❌';
    }

    setupAutoRefresh() {
        this.intervals.push(
            setInterval(() => {
                this.loadAllEndpoints();
            }, this.updateInterval)
        );
    }

    refreshAll() {
        console.log('🔄 Manual refresh triggered');
        this.loadAllEndpoints();
    }

    viewDetails(key) {
        const data = this.dashboardData[key];
        if (!data) return;
        
        const modal = document.getElementById('details-modal');
        const title = document.getElementById('modal-title');
        const body = document.getElementById('modal-body');
        
        title.textContent = `${key.charAt(0).toUpperCase() + key.slice(1)} - Full Data`;
        body.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
        
        modal.style.display = 'flex';
    }

    closeDetails() {
        document.getElementById('details-modal').style.display = 'none';
    }

    toggleSettings() {
        const panel = document.getElementById('settings-panel');
        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    }

    updateRefreshInterval(newInterval) {
        this.updateInterval = parseInt(newInterval);
        
        // Clear existing intervals
        this.intervals.forEach(interval => clearInterval(interval));
        this.intervals = [];
        
        // Set up new interval
        this.setupAutoRefresh();
        
        console.log(`Refresh interval updated to ${this.updateInterval}ms`);
    }

    toggleAutoRefresh(enabled) {
        if (enabled) {
            this.setupAutoRefresh();
        } else {
            this.intervals.forEach(interval => clearInterval(interval));
            this.intervals = [];
        }
    }

    destroy() {
        // Clean up intervals
        this.intervals.forEach(interval => clearInterval(interval));
        this.intervals = [];
    }
}

// Initialize dashboard
let backendDashboard;

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        backendDashboard = new BackendDashboard();
    });
} else {
    backendDashboard = new BackendDashboard();
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BackendDashboard;
} 