/**
 * Time Slice Selector for Historical Orca Sightings
 * Simple component with 5 time scales: hours, days, weeks, months, years
 * 15 time units scrubbing capability, flushed right to current time
 */

class TimeSliceSelector {
    constructor() {
        this.timeScales = [
            { label: 'Hours', unit: 'hours', maxValue: 15 },
            { label: 'Days', unit: 'days', maxValue: 15 },
            { label: 'Weeks', unit: 'weeks', maxValue: 15 },
            { label: 'Months', unit: 'months', maxValue: 15 },
            { label: 'Years', unit: 'years', maxValue: 15 }
        ];
        
        this.currentScale = 'days'; // Default scale
        this.currentValue = 1; // Default to 1 unit
        this.currentPosition = 0; // 0 = flushed right (most current), 15 = furthest back
        
        this.onTimeSliceChange = null; // Callback for when slice changes
    }

    /**
     * Create the time slice selector interface
     */
    createSelectorInterface() {
        return `
            <div class="time-slice-selector">
                <div class="selector-header">
                    <h3>📊 Historical Sightings Timeline</h3>
                    <div class="current-window" id="current-window-display">
                        Last ${this.currentValue} ${this.currentScale}
                    </div>
                </div>
                
                <!-- Time Scale Buttons -->
                <div class="time-scale-buttons">
                    ${this.timeScales.map(scale => `
                        <button class="scale-btn ${scale.unit === this.currentScale ? 'active' : ''}" 
                                onclick="timeSliceSelector.setTimeScale('${scale.unit}')">
                            ${scale.label}
                        </button>
                    `).join('')}
                </div>
                
                <!-- Time Value Slider -->
                <div class="time-value-control">
                    <label>Time Window Size:</label>
                    <div class="slider-container">
                        <span class="slider-label">1</span>
                        <input type="range" 
                               id="time-value-slider" 
                               min="1" 
                               max="15" 
                               value="${this.currentValue}"
                               oninput="timeSliceSelector.setTimeValue(this.value)">
                        <span class="slider-label">15</span>
                    </div>
                    <div class="value-display">${this.currentValue} ${this.currentScale}</div>
                </div>
                
                <!-- Position Scrubber -->
                <div class="position-control">
                    <label>Time Position:</label>
                    <div class="scrubber-container">
                        <span class="position-label">Now</span>
                        <input type="range" 
                               id="position-scrubber" 
                               min="0" 
                               max="15" 
                               value="${this.currentPosition}"
                               oninput="timeSliceSelector.setPosition(this.value)">
                        <span class="position-label">-15</span>
                    </div>
                    <div class="position-display" id="position-display">
                        ${this.getPositionDescription()}
                    </div>
                </div>
                
                <!-- Date Range Display -->
                <div class="date-range-display">
                    <div class="range-info">
                        <strong>Viewing:</strong> <span id="date-range-text">${this.getDateRangeText()}</span>
                    </div>
                    <button class="apply-btn" onclick="timeSliceSelector.applyTimeSlice()">
                        Apply Time Slice
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Create the CSS styles for the selector
     */
    createSelectorStyles() {
        return `
            <style>
                .time-slice-selector {
                    background: white;
                    border-radius: 12px;
                    padding: 20px;
                    margin: 15px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                    border: 1px solid #e2e8f0;
                }

                .selector-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                    padding-bottom: 15px;
                    border-bottom: 2px solid #f0f0f0;
                }

                .selector-header h3 {
                    margin: 0;
                    color: #2d3748;
                    font-size: 1.3em;
                }

                .current-window {
                    background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-weight: 600;
                    font-size: 0.9em;
                }

                .time-scale-buttons {
                    display: flex;
                    gap: 8px;
                    margin-bottom: 25px;
                    flex-wrap: wrap;
                }

                .scale-btn {
                    background: #f7fafc;
                    border: 2px solid #e2e8f0;
                    color: #4a5568;
                    padding: 10px 16px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: 500;
                    transition: all 0.3s ease;
                    flex: 1;
                    min-width: 80px;
                }

                .scale-btn:hover {
                    background: #edf2f7;
                    border-color: #cbd5e0;
                }

                .scale-btn.active {
                    background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
                    color: white;
                    border-color: #3182ce;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
                }

                .time-value-control, .position-control {
                    margin-bottom: 20px;
                }

                .time-value-control label, .position-control label {
                    display: block;
                    font-weight: 600;
                    color: #2d3748;
                    margin-bottom: 10px;
                }

                .slider-container, .scrubber-container {
                    display: flex;
                    align-items: center;
                    gap: 15px;
                    margin-bottom: 8px;
                }

                .slider-label, .position-label {
                    font-size: 0.9em;
                    font-weight: 500;
                    color: #718096;
                    min-width: 30px;
                    text-align: center;
                }

                input[type="range"] {
                    flex: 1;
                    height: 6px;
                    border-radius: 3px;
                    background: #e2e8f0;
                    outline: none;
                    -webkit-appearance: none;
                }

                input[type="range"]::-webkit-slider-thumb {
                    -webkit-appearance: none;
                    appearance: none;
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
                    cursor: pointer;
                    border: 2px solid white;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
                }

                input[type="range"]::-moz-range-thumb {
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
                    cursor: pointer;
                    border: 2px solid white;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
                }

                .value-display, .position-display {
                    text-align: center;
                    font-weight: 600;
                    color: #2d3748;
                    background: #f7fafc;
                    padding: 8px 12px;
                    border-radius: 6px;
                    border: 1px solid #e2e8f0;
                }

                .date-range-display {
                    background: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 15px;
                    text-align: center;
                }

                .range-info {
                    margin-bottom: 15px;
                    font-size: 1.1em;
                }

                .apply-btn {
                    background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 8px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    font-size: 1em;
                }

                .apply-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(72, 187, 120, 0.3);
                }

                /* Responsive */
                @media (max-width: 768px) {
                    .selector-header {
                        flex-direction: column;
                        gap: 10px;
                        text-align: center;
                    }
                    
                    .time-scale-buttons {
                        justify-content: center;
                    }
                    
                    .scale-btn {
                        min-width: 60px;
                        padding: 8px 12px;
                        font-size: 0.9em;
                    }
                }
            </style>
        `;
    }

    /**
     * Set the time scale (hours, days, weeks, months, years)
     */
    setTimeScale(scale) {
        this.currentScale = scale;
        this.updateDisplay();
        this.updateActiveButton(scale);
    }

    /**
     * Set the time value (1-15 units)
     */
    setTimeValue(value) {
        this.currentValue = parseInt(value);
        this.updateDisplay();
    }

    /**
     * Set the position (0=now, 15=furthest back)
     */
    setPosition(position) {
        this.currentPosition = parseInt(position);
        this.updateDisplay();
    }

    /**
     * Update active button styling
     */
    updateActiveButton(activeScale) {
        document.querySelectorAll('.scale-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[onclick="timeSliceSelector.setTimeScale('${activeScale}')"]`).classList.add('active');
    }

    /**
     * Update all display elements
     */
    updateDisplay() {
        // Update current window display
        document.getElementById('current-window-display').textContent = 
            `Last ${this.currentValue} ${this.currentScale}`;
        
        // Update value display
        document.querySelector('.value-display').textContent = 
            `${this.currentValue} ${this.currentScale}`;
        
        // Update position display
        document.getElementById('position-display').textContent = 
            this.getPositionDescription();
        
        // Update date range
        document.getElementById('date-range-text').textContent = 
            this.getDateRangeText();
    }

    /**
     * Get description of current position
     */
    getPositionDescription() {
        if (this.currentPosition === 0) {
            return 'Current time window';
        } else {
            return `${this.currentPosition} ${this.currentScale} ago`;
        }
    }

    /**
     * Get the actual date range text
     */
    getDateRangeText() {
        const now = new Date();
        const endDate = this.calculateEndDate(now);
        const startDate = this.calculateStartDate(endDate);
        
        const formatOptions = this.getFormatOptions();
        
        return `${startDate.toLocaleDateString('en-US', formatOptions)} - ${endDate.toLocaleDateString('en-US', formatOptions)}`;
    }

    /**
     * Calculate the end date based on position
     */
    calculateEndDate(now) {
        const endDate = new Date(now);
        
        switch (this.currentScale) {
            case 'hours':
                endDate.setHours(endDate.getHours() - this.currentPosition);
                break;
            case 'days':
                endDate.setDate(endDate.getDate() - this.currentPosition);
                break;
            case 'weeks':
                endDate.setDate(endDate.getDate() - (this.currentPosition * 7));
                break;
            case 'months':
                endDate.setMonth(endDate.getMonth() - this.currentPosition);
                break;
            case 'years':
                endDate.setFullYear(endDate.getFullYear() - this.currentPosition);
                break;
        }
        
        return endDate;
    }

    /**
     * Calculate the start date based on end date and time value
     */
    calculateStartDate(endDate) {
        const startDate = new Date(endDate);
        
        switch (this.currentScale) {
            case 'hours':
                startDate.setHours(startDate.getHours() - this.currentValue);
                break;
            case 'days':
                startDate.setDate(startDate.getDate() - this.currentValue);
                break;
            case 'weeks':
                startDate.setDate(startDate.getDate() - (this.currentValue * 7));
                break;
            case 'months':
                startDate.setMonth(startDate.getMonth() - this.currentValue);
                break;
            case 'years':
                startDate.setFullYear(startDate.getFullYear() - this.currentValue);
                break;
        }
        
        return startDate;
    }

    /**
     * Get format options based on time scale
     */
    getFormatOptions() {
        switch (this.currentScale) {
            case 'hours':
                return { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' };
            case 'days':
                return { month: 'short', day: 'numeric', year: 'numeric' };
            case 'weeks':
                return { month: 'short', day: 'numeric', year: 'numeric' };
            case 'months':
                return { month: 'long', year: 'numeric' };
            case 'years':
                return { year: 'numeric' };
            default:
                return { month: 'short', day: 'numeric', year: 'numeric' };
        }
    }

    /**
     * Apply the current time slice selection
     */
    applyTimeSlice() {
        const now = new Date();
        const endDate = this.calculateEndDate(now);
        const startDate = this.calculateStartDate(endDate);
        
        const timeSlice = {
            scale: this.currentScale,
            value: this.currentValue,
            position: this.currentPosition,
            startDate: startDate.toISOString(),
            endDate: endDate.toISOString(),
            description: `${this.currentValue} ${this.currentScale} ${this.currentPosition > 0 ? `(${this.currentPosition} periods ago)` : '(current)'}`
        };
        
        console.log('🕒 Applied time slice:', timeSlice);
        
        // Emit event for other components to listen to
        window.dispatchEvent(new CustomEvent('timeSliceChanged', {
            detail: { timeSlice }
        }));
        
        // Call callback if set
        if (this.onTimeSliceChange) {
            this.onTimeSliceChange(timeSlice);
        }
        
        // Show confirmation
        this.showApplyConfirmation();
    }

    /**
     * Show confirmation that time slice was applied
     */
    showApplyConfirmation() {
        const btn = document.querySelector('.apply-btn');
        const originalText = btn.textContent;
        
        btn.textContent = '✓ Applied!';
        btn.style.background = 'linear-gradient(135deg, #48bb78 0%, #38a169 100%)';
        
        setTimeout(() => {
            btn.textContent = originalText;
            btn.style.background = 'linear-gradient(135deg, #48bb78 0%, #38a169 100%)';
        }, 1500);
    }

    /**
     * Get current time slice configuration
     */
    getCurrentTimeSlice() {
        const now = new Date();
        const endDate = this.calculateEndDate(now);
        const startDate = this.calculateStartDate(endDate);
        
        return {
            scale: this.currentScale,
            value: this.currentValue,
            position: this.currentPosition,
            startDate: startDate.toISOString(),
            endDate: endDate.toISOString()
        };
    }

    /**
     * Set callback for time slice changes
     */
    setOnTimeSliceChange(callback) {
        this.onTimeSliceChange = callback;
    }
}

// Initialize global instance
let timeSliceSelector;

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        timeSliceSelector = new TimeSliceSelector();
    });
} else {
    timeSliceSelector = new TimeSliceSelector();
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TimeSliceSelector;
} 