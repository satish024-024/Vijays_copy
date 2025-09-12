// Quantum Spark - Modern Dashboard
// Enhanced version of HackathonDashboard with modern UI features
class ModernDashboard extends HackathonDashboard {
    constructor() {
        super();
        this.modernFeatures = {
            enhancedVisualizations: true,
            realTimeUpdates: true,
            advancedMetrics: true,
            predictiveAnalytics: true
        };
        console.log('🚀 Modern Dashboard initialized with enhanced IBM Quantum data integration');
    }

    // Override fetchDashboardData to include modern-specific enhancements
    async fetchDashboardData() {
        try {
            console.log('🔄 Modern Dashboard: Fetching comprehensive IBM Quantum data with enhanced analytics...');

            // Fetch all enhanced APIs concurrently (same as hackathon but with modern logging)
            const [
                dashboardResponse,
                backendsResponse,
                jobsResponse,
                jobResultsResponse,
                performanceResponse,
                realtimeResponse,
                circuitDetailsResponse,
                historicalResponse,
                calibrationResponse,
                dashboardMetricsResponse
            ] = await Promise.allSettled([
                fetch('/api/dashboard_state'),
                fetch('/api/backends'),
                fetch('/api/jobs'),
                fetch('/api/job_results'),
                fetch('/api/performance_metrics'),
                fetch('/api/realtime_monitoring'),
                fetch('/api/circuit_details'),
                fetch('/api/historical_data'),
                fetch('/api/calibration_data'),
                fetch('/api/dashboard_metrics')
            ]);

            // Process responses (same logic as hackathon)
            const dashboardData = dashboardResponse.status === 'fulfilled' && dashboardResponse.value.ok
                ? await dashboardResponse.value.json()
                : {};

            const backendsData = backendsResponse.status === 'fulfilled' && backendsResponse.value.ok
                ? await backendsResponse.value.json()
                : [];

            const jobsData = jobsResponse.status === 'fulfilled' && jobsResponse.value.ok
                ? await jobsResponse.value.json()
                : [];

            const jobResultsData = jobResultsResponse.status === 'fulfilled' && jobResultsResponse.value.ok
                ? await jobResultsResponse.value.json()
                : [];

            const performanceData = performanceResponse.status === 'fulfilled' && performanceResponse.value.ok
                ? await performanceResponse.value.json()
                : {};

            const realtimeData = realtimeResponse.status === 'fulfilled' && realtimeResponse.value.ok
                ? await realtimeResponse.value.json()
                : {};

            const circuitDetailsData = circuitDetailsResponse.status === 'fulfilled' && circuitDetailsResponse.value.ok
                ? await circuitDetailsResponse.value.json()
                : [];

            const historicalData = historicalResponse.status === 'fulfilled' && historicalResponse.value.ok
                ? await historicalResponse.value.json()
                : {};

            const calibrationData = calibrationResponse.status === 'fulfilled' && calibrationResponse.value.ok
                ? await calibrationResponse.value.json()
                : {};

            const dashboardMetricsData = dashboardMetricsResponse.status === 'fulfilled' && dashboardMetricsResponse.value.ok
                ? await dashboardMetricsResponse.value.json()
                : {};

            // Update state with comprehensive data
            this.state = {
                ...this.state,
                backends: Array.isArray(backendsData) ? backendsData : (backendsData.backends || []),
                jobs: Array.isArray(jobsData) ? jobsData : (jobsData.jobs || []),
                jobResults: Array.isArray(jobResultsData) ? jobResultsData : [],
                performance: performanceData,
                realtime: realtimeData,
                circuitDetails: Array.isArray(circuitDetailsData) ? circuitDetailsData : [],
                historical: historicalData,
                calibration: calibrationData,
                dashboardMetrics: dashboardMetricsData,
                metrics: dashboardData.metrics || {},
                isConnected: dashboardData.connection_status?.is_connected || false
            };

            // Modern-specific logging
            console.log('✨ Modern Dashboard: Comprehensive IBM Quantum data loaded:', {
                backendsCount: this.state.backends.length,
                jobsCount: this.state.jobs.length,
                jobResultsCount: this.state.jobResults.length,
                performanceMetrics: Object.keys(this.state.performance).length,
                realtimeMetrics: Object.keys(this.state.realtime).length,
                circuitDetailsCount: this.state.circuitDetails.length,
                historicalTrends: Object.keys(this.state.historical).length,
                calibrationStatus: Object.keys(this.state.calibration).length,
                connected: this.state.isConnected
            });

            // Update connection status
            this.updateConnectionStatus(dashboardData.connection_status?.is_connected || false);

            // Update enhanced metrics with modern styling
            this.updateModernMetrics();

            // Enable modern features
            this.enableModernFeatures();

        } catch (error) {
            console.error('❌ Modern Dashboard: Error fetching comprehensive data:', error);
            throw new Error('Failed to fetch comprehensive IBM Quantum data: ' + error.message);
        }
    }

    updateModernMetrics() {
        console.log('📊 Modern Dashboard: Updating enhanced metrics with modern styling...');

        // Update basic metrics with enhanced data
        const activeBackends = this.state.backends.filter(b => b.status === 'active' || b.operational).length;
        const totalJobs = this.state.dashboardMetrics.total_jobs || this.state.jobs.length;
        const runningJobs = this.state.dashboardMetrics.running_jobs || this.state.jobs.filter(j => j.status === 'running').length;

        // Update DOM elements with modern animations
        const updateElement = (id, value, fallback = '0') => {
            const element = document.getElementById(id);
            if (element) {
                // Add modern animation effect
                element.style.transition = 'all 0.3s ease';
                element.style.transform = 'scale(0.95)';
                element.textContent = value || fallback;

                setTimeout(() => {
                    element.style.transform = 'scale(1)';
                }, 50);
            }
        };

        updateElement('active-backends', activeBackends);
        updateElement('total-jobs', totalJobs);
        updateElement('running-jobs', runningJobs);

        // Update success rate with enhanced calculation
        const successRate = this.calculateEnhancedSuccessRate();
        updateElement('success-rate', `${successRate}%`);

        // Update additional modern metrics
        if (this.state.dashboardMetrics.success_rate !== undefined) {
            updateElement('success-rate', `${this.state.dashboardMetrics.success_rate}%`);
        }

        // Update performance metrics with modern formatting
        if (this.state.performance && Object.keys(this.state.performance).length > 0) {
            updateElement('avg-execution-time', `${this.state.performance.average_execution_time?.toFixed(1) || 'N/A'}s`);
            updateElement('avg-queue-time', `${this.state.performance.average_queue_time?.toFixed(1) || 'N/A'}s`);
            updateElement('avg-fidelity', `${(this.state.performance.average_fidelity * 100)?.toFixed(1) || 'N/A'}%`);
        }

        // Update real-time metrics with modern styling
        if (this.state.realtime && Object.keys(this.state.realtime).length > 0) {
            updateElement('queue-position', this.state.realtime.system_status?.total_pending_jobs || '0');
            updateElement('estimated-wait', `${this.state.realtime.system_status?.average_queue_time?.toFixed(0) || 'N/A'}s`);
        }

        // Update calibration status with modern indicators
        if (this.state.calibration && Object.keys(this.state.calibration).length > 0) {
            updateElement('calibration-status', this.state.calibration.calibration_status || 'Unknown');
            updateElement('system-health', this.state.calibration.system_health?.overall_status || 'Unknown');
        }

        // Update historical trends
        if (this.state.historical && Object.keys(this.state.historical).length > 0) {
            updateElement('total-jobs-analyzed', this.state.historical.total_jobs || '0');
            updateElement('success-trend', this.state.historical.success_trend?.slice(-1)[0]?.toFixed(1) || 'N/A');
        }

        console.log('✅ Modern Dashboard: Enhanced metrics updated with modern styling');
    }

    enableModernFeatures() {
        // Enable modern-specific features
        this.enableRealTimeUpdates();
        this.enablePredictiveAnalytics();
        this.enableAdvancedVisualizations();

        console.log('🎨 Modern Dashboard: Enhanced features enabled');
    }

    enableRealTimeUpdates() {
        // Set up more frequent updates for modern dashboard
        if (this.modernFeatures.realTimeUpdates) {
            this.refreshIntervalMs = 15000; // 15 seconds for modern dashboard
            this.restartAutoRefresh();
        }
    }

    enablePredictiveAnalytics() {
        if (this.modernFeatures.predictiveAnalytics) {
            // Add predictive analytics based on historical data
            this.predictJobCompletionTimes();
            this.predictBackendAvailability();
        }
    }

    enableAdvancedVisualizations() {
        if (this.modernFeatures.enhancedVisualizations) {
            // Enhance visualizations with modern styling
            this.enhanceWidgetVisualizations();
        }
    }

    predictJobCompletionTimes() {
        // Use historical data to predict job completion times
        if (this.state.historical && this.state.performance) {
            const historicalExecutionTimes = this.state.performance.execution_times || [];
            const avgExecutionTime = this.state.performance.average_execution_time;

            if (avgExecutionTime && historicalExecutionTimes.length > 0) {
                // Simple prediction based on moving average
                const predictedTime = this.calculateMovingAverage(historicalExecutionTimes.slice(-5));
                console.log(`🔮 Predicted job completion time: ${predictedTime.toFixed(1)}s`);

                // Update prediction display if element exists
                const predictionElement = document.getElementById('predicted-completion-time');
                if (predictionElement) {
                    predictionElement.textContent = `${predictedTime.toFixed(1)}s`;
                }
            }
        }
    }

    predictBackendAvailability() {
        // Predict backend availability based on queue patterns
        if (this.state.realtime && this.state.historical) {
            const queueTimes = this.state.realtime.system_status?.average_queue_time || 0;
            const backendUsage = this.state.historical.backend_usage || {};

            // Simple availability prediction
            const totalBackends = Object.keys(backendUsage).length;
            const busyBackends = Object.values(backendUsage).filter(usage => usage > 5).length;

            const availability = totalBackends > 0 ? ((totalBackends - busyBackends) / totalBackends) * 100 : 0;
            console.log(`🔮 Predicted backend availability: ${availability.toFixed(1)}%`);

            // Update availability display if element exists
            const availabilityElement = document.getElementById('backend-availability');
            if (availabilityElement) {
                availabilityElement.textContent = `${availability.toFixed(1)}%`;
            }
        }
    }

    calculateMovingAverage(data) {
        if (data.length === 0) return 0;
        const sum = data.reduce((a, b) => a + b, 0);
        return sum / data.length;
    }

    enhanceWidgetVisualizations() {
        // Add modern styling to widgets
        const widgets = document.querySelectorAll('.widget');
        widgets.forEach((widget, index) => {
            // Add modern gradient backgrounds
            widget.style.background = 'var(--surface-gradient)';
            widget.style.backdropFilter = 'blur(20px)';
            widget.style.border = '1px solid var(--glass-border)';

            // Add hover effects
            widget.addEventListener('mouseenter', () => {
                widget.style.transform = 'translateY(-2px)';
                widget.style.boxShadow = 'var(--shadow-glow)';
            });

            widget.addEventListener('mouseleave', () => {
                widget.style.transform = 'translateY(0)';
                widget.style.boxShadow = 'var(--shadow-deep)';
            });
        });
    }

    restartAutoRefresh() {
        // Clear existing timer
        if (this.countdownTimerId) {
            clearInterval(this.countdownTimerId);
        }

        // Restart with new interval
        this.startAutoRefresh();
    }

    // Override AI response for modern context
    async simulateAIResponse(query) {
        // Enhanced AI responses for modern dashboard
        const lowerQuery = query.toLowerCase();

        if (lowerQuery.includes('performance') || lowerQuery.includes('metrics')) {
            const successRate = this.calculateEnhancedSuccessRate();
            const avgExecutionTime = this.state.performance?.average_execution_time?.toFixed(1) || 'N/A';
            return `Based on the current IBM Quantum data, your system shows a ${successRate}% success rate with an average execution time of ${avgExecutionTime} seconds. The calibration status is ${this.state.calibration?.calibration_status || 'unknown'} and system health is ${this.state.calibration?.system_health?.overall_status || 'unknown'}.`;
        } else if (lowerQuery.includes('prediction') || lowerQuery.includes('forecast')) {
            return "Using historical trends and current queue data, I can predict job completion times and backend availability. The system analyzes patterns from recent job executions to provide accurate forecasts for optimal quantum computing scheduling.";
        } else if (lowerQuery.includes('real') || lowerQuery.includes('live')) {
            return "This modern dashboard provides real-time data from IBM Quantum APIs, including live backend status, queue positions, calibration data, and performance metrics. All data is fetched directly from IBM Quantum services for maximum accuracy.";
        } else {
            return "The modern dashboard integrates comprehensive IBM Quantum data including performance metrics, real-time monitoring, calibration status, and predictive analytics. What specific aspect would you like to explore?";
        }
    }
}

// Initialize Modern Dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎨 Initializing Modern Dashboard with enhanced IBM Quantum integration...');
    window.dashboard = new ModernDashboard();
});
