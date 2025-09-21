// Backend Comparison and Queue Management System
// Provides detailed comparison of quantum backends and queue optimization

class BackendComparisonSystem {
    constructor() {
        this.backends = new Map();
        this.queueHistory = new Map();
        this.comparisonData = null;
        this.updateInterval = null;
        
        this.init();
    }

    init() {
        console.log('🔄 Initializing Backend Comparison System...');
        this.injectComparisonStyles();
        this.setupComparisonInterface();
        this.startDataCollection();
        this.createComparisonWidget();
    }

    setupComparisonInterface() {
        // Add comparison button to backends widget (supports multiple dashboard templates)
        const backendsWidget = document.querySelector('.backends-widget .widget-controls')
            || document.querySelector('[data-widget="backends"] .widget-controls');
        if (backendsWidget && !backendsWidget.querySelector('.compare-btn')) {
            const compareBtn = document.createElement('button');
            compareBtn.className = 'widget-btn compare-btn';
            compareBtn.innerHTML = '<i class="fas fa-balance-scale"></i>';
            compareBtn.title = 'Compare Backends';
            compareBtn.addEventListener('click', () => this.showComparisonModal());
            backendsWidget.appendChild(compareBtn);
        }
    }

    injectComparisonStyles() {
        if (document.getElementById('comparison-styles')) return;
        const style = document.createElement('style');
        style.id = 'comparison-styles';
        style.textContent = `
            .comparison-modal{position:fixed;inset:0;background:rgba(0,0,0,0.8);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;z-index:1700;opacity:0;visibility:hidden;transition:all .3s ease}
            .comparison-modal.active{opacity:1;visibility:visible}
            .comparison-modal .modal-content{background:rgba(20,20,30,0.95);border:1px solid rgba(255,255,255,0.15);border-radius:16px;max-width:90vw;max-height:90vh;width:1200px;overflow:auto;box-shadow:0 16px 64px rgba(0,0,0,0.45)}
            .comparison-modal .modal-header{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid rgba(255,255,255,0.1);color:#fff}
            .comparison-modal .modal-body{padding:16px;color:#e0e0e0}
            .comparison-controls{display:flex;align-items:center;gap:12px;margin-bottom:16px}
            .comparison-table{width:100%;border-collapse:collapse}
            .comparison-table th{background:rgba(0,245,255,0.08);color:#fff;text-align:left;padding:12px;border-bottom:1px solid rgba(255,255,255,0.1)}
            .comparison-table td{padding:12px;border-bottom:1px solid rgba(255,255,255,0.06)}
            .refresh-btn{padding:8px 12px;border:none;border-radius:8px;background:linear-gradient(135deg,#00f5ff,#00d4ff);color:#000;cursor:pointer}
        `;
        document.head.appendChild(style);
    }

    createComparisonWidget() {
        // Create comparison modal
        const modal = document.createElement('div');
        modal.id = 'backend-comparison-modal';
        modal.className = 'comparison-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2><i class="fas fa-balance-scale"></i> Backend Comparison</h2>
                    <button class="close-btn" id="close-comparison-modal">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="comparison-controls">
                        <div class="filter-section">
                            <label>Filter by Status:</label>
                            <select id="status-filter">
                                <option value="all">All Backends</option>
                                <option value="online">Online Only</option>
                                <option value="offline">Offline Only</option>
                            </select>
                        </div>
                        <div class="sort-section">
                            <label>Sort by:</label>
                            <select id="sort-option">
                                <option value="queue">Queue Length</option>
                                <option value="wait">Predicted Wait</option>
                                <option value="qubits">Number of Qubits</option>
                                <option value="performance">Score</option>
                            </select>
                        </div>
                        <div class="sort-section">
                            <label>Algorithm:</label>
                            <select id="algo-option">
                                <option value="auto">Auto</option>
                                <option value="balanced">Balanced</option>
                                <option value="fastest_queue">Fastest Queue</option>
                                <option value="low_latency">Low Latency</option>
                                <option value="highest_qubits">Highest Qubits</option>
                            </select>
                        </div>
                        <div class="sort-section">
                            <label>Complexity:</label>
                            <select id="complexity-option">
                                <option value="low">Low</option>
                                <option value="medium" selected>Medium</option>
                                <option value="high">High</option>
                            </select>
                        </div>
                        <button class="refresh-btn" id="refresh-comparison">
                            <i class="fas fa-sync-alt"></i> Refresh
                        </button>
                    </div>
                    <div class="comparison-table-container">
                        <table class="comparison-table" id="comparison-table">
                            <thead>
                                <tr>
                                    <th>Backend</th>
                                    <th>Status</th>
                                    <th>Qubits</th>
                                    <th>Queue</th>
                                    <th>Execution Time</th>
                                    <th>Success Rate</th>
                                    <th>Fidelity</th>
                                    <th>Calibration</th>
                                    <th>Gate Error</th>
                                    <th>Coherence</th>
                                    <th>Usage</th>
                                    <th>Recommendation</th>
                                </tr>
                            </thead>
                            <tbody id="comparison-tbody">
                                <!-- Comparison data will be populated here -->
                            </tbody>
                        </table>
                    </div>
                    <div class="comparison-insights">
                        <h3>💡 Insights & Recommendations</h3>
                        <div class="insights-content" id="insights-content">
                            <!-- AI-generated insights will appear here -->
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Setup event listeners
        this.setupComparisonEventListeners();
    }

    setupComparisonEventListeners() {
        const closeBtn = document.getElementById('close-comparison-modal');
        const refreshBtn = document.getElementById('refresh-comparison');
        const statusFilter = document.getElementById('status-filter');
        const sortOption = document.getElementById('sort-option');
        const algoOption = document.getElementById('algo-option');
        const complexityOption = document.getElementById('complexity-option');

        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.closeComparisonModal());
        }

        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshComparisonData());
        }

        if (statusFilter) {
            statusFilter.addEventListener('change', () => this.filterAndSortBackends());
        }

        if (sortOption) sortOption.addEventListener('change', () => this.filterAndSortBackends());
        if (algoOption) algoOption.addEventListener('change', () => this.collectBackendData());
        if (complexityOption) complexityOption.addEventListener('change', () => this.collectBackendData());
    }

    startDataCollection() {
        // Collect backend data every 10 seconds from real endpoints
        this.updateInterval = setInterval(() => {
            this.collectBackendData();
        }, 10000);
        // Initial data collection
        this.collectBackendData();
    }

    async collectBackendData() {
        try {
            const backendData = await this.fetchBackendData();
            
            backendData.forEach(backend => {
                const backendName = backend.name;
                
                // Store current state
                this.backends.set(backendName, {
                    ...backend,
                    timestamp: Date.now()
                });
                
                // Store queue history
                if (!this.queueHistory.has(backendName)) {
                    this.queueHistory.set(backendName, []);
                }
                
                const history = this.queueHistory.get(backendName);
                history.push({
                    queue: backend.queue,
                    timestamp: Date.now()
                });
                
                // Keep only last 100 entries
                if (history.length > 100) {
                    history.shift();
                }
            });
            
            // Update comparison data
            this.updateComparisonData();
            
        } catch (error) {
            console.error('Failed to collect backend data:', error);
            this.showNotification('Failed to load real backend data', 'error');
        }
    }

    async fetchBackendData() {
        console.log('🔄 Backend Comparison: Fetching comprehensive data from all enhanced IBM Quantum APIs...');

        // Fetch real data from all enhanced backend APIs
        const algo = document.getElementById('algo-option')?.value || 'auto';
        const complexity = document.getElementById('complexity-option')?.value || 'medium';

        // Fetch all enhanced APIs concurrently
        const [
            backendsRes,
            performanceRes,
            realtimeRes,
            calibrationRes,
            historicalRes,
            predsRes,
            recsRes
        ] = await Promise.allSettled([
            fetch('/api/backends'),
            fetch('/api/performance_metrics'),
            fetch('/api/realtime_monitoring'),
            fetch('/api/calibration_data'),
            fetch('/api/historical_data'),
            fetch(`/api/predictions?job_complexity=${encodeURIComponent(complexity)}`),
            fetch(`/api/recommendations?algorithm=${encodeURIComponent(algo)}&top_k=999&job_complexity=${encodeURIComponent(complexity)}`)
        ]);

        // Process responses with error handling
        const backendsJson = backendsRes.status === 'fulfilled' && backendsRes.value.ok
            ? await backendsRes.value.json()
            : [];

        const performanceJson = performanceRes.status === 'fulfilled' && performanceRes.value.ok
            ? await performanceRes.value.json()
            : {};

        const realtimeJson = realtimeRes.status === 'fulfilled' && realtimeRes.value.ok
            ? await realtimeRes.value.json()
            : {};

        const calibrationJson = calibrationRes.status === 'fulfilled' && calibrationRes.value.ok
            ? await calibrationRes.value.json()
            : {};

        const historicalJson = historicalRes.status === 'fulfilled' && historicalRes.value.ok
            ? await historicalRes.value.json()
            : {};

        const predsJson = predsRes.status === 'fulfilled' && predsRes.value.ok
            ? await predsRes.value.json()
            : { predictions: [] };

        const recsJson = recsRes.status === 'fulfilled' && recsRes.value.ok
            ? await recsRes.value.json()
            : { recommendations: [] };

        // Process enhanced data
        const predictions = Array.isArray(predsJson.predictions) ? predsJson.predictions : [];
        const recommendations = Array.isArray(recsJson.recommendations) ? recsJson.recommendations : [];

        const predByName = new Map(predictions.map(p => [p.name, p]));
        const rankByName = new Map(recommendations.map((r, i) => [r.name, { score: r.score, rank: i + 1, wait: r.predicted_wait_seconds, throughput: r.throughput_jobs_per_hour, explanation: r.explanation, algorithm: r.algorithm }]));

        // Get backend-specific performance data
        const backendPerformance = performanceJson.backend_performance || {};
        const backendCalibrations = calibrationJson.backend_calibrations || {};
        const backendUsage = historicalJson.backend_usage || {};

        const items = (Array.isArray(backendsJson) ? backendsJson : []).map(b => {
            const name = b.name || 'unknown';
            const pred = predByName.get(name);
            const rinfo = rankByName.get(name) || {};
            const perf = backendPerformance[name] || {};
            const calib = backendCalibrations[name] || {};
            const usage = backendUsage[name] || 0;

            // Calculate enhanced metrics
            const gateErrors = b.gate_errors || {};
            const avgGateError = Object.keys(gateErrors).length > 0
                ? Object.values(gateErrors).reduce((sum, err) => sum + err, 0) / Object.keys(gateErrors).length
                : 0;

            const t1Times = b.t1_times || {};
            const avgT1 = Object.keys(t1Times).length > 0
                ? Object.values(t1Times).reduce((sum, t1) => sum + t1, 0) / Object.keys(t1Times).length
                : 0;

            return {
                name,
                status: b.operational ? 'online' : 'offline',
                qubits: typeof b.num_qubits === 'number' ? b.num_qubits : (b.num_qubits || 0),
                queue: typeof b.pending_jobs === 'number' ? b.pending_jobs : (b.pending_jobs || 0),
                avgWaitTime: typeof (rinfo.wait ?? pred?.predicted_wait_seconds) === 'number' ? (rinfo.wait ?? pred?.predicted_wait_seconds) : 0,
                throughput: typeof (rinfo.throughput ?? pred?.throughput_jobs_per_hour) === 'number' ? (rinfo.throughput ?? pred?.throughput_jobs_per_hour) : 0,
                performanceScore: typeof rinfo.score === 'number' ? Math.round(rinfo.score * 100) : 0,
                recommendationRank: typeof rinfo.rank === 'number' ? rinfo.rank : null,
                explanation: rinfo.explanation || null,
                algorithm: rinfo.algorithm || (document.getElementById('algo-option')?.value || 'auto'),

                // Enhanced metrics from new APIs
                avgExecutionTime: perf.average_execution_time || 0,
                successRate: perf.success_rate ? Math.round(perf.success_rate * 100) : 0,
                avgFidelity: perf.average_fidelity ? Math.round(perf.average_fidelity * 100) : 0,
                calibrationStatus: calib.status || 'unknown',
                calibrationQuality: calib.calibration_quality ? Math.round(calib.calibration_quality * 100) : 0,
                usageCount: usage,
                gateErrorRate: avgGateError,
                coherenceTime: avgT1,
                couplingMapSize: (b.coupling_map || []).length,
                basisGatesCount: (b.basis_gates || []).length,

                lastUpdate: Date.now()
            };
        });

        console.log(`✅ Backend Comparison: Loaded comprehensive data for ${items.length} backends`);
        return items;
    }

    formatThroughput(value) {
        if (!value) return '—';
        return `${value.toFixed(1)} jobs/h`;
    }

    updateComparisonData() {
        this.comparisonData = Array.from(this.backends.values());
        this.filterAndSortBackends();
        this.generateInsights();
    }

    filterAndSortBackends() {
        const statusFilter = document.getElementById('status-filter')?.value || 'all';
        const sortOption = document.getElementById('sort-option')?.value || 'queue';
        
        let filteredData = [...this.comparisonData];
        
        // Apply status filter
        if (statusFilter !== 'all') {
            filteredData = filteredData.filter(backend => backend.status === statusFilter);
        }
        
        // Apply sorting
        filteredData.sort((a, b) => {
            switch (sortOption) {
                case 'queue':
                    return a.queue - b.queue;
                case 'wait':
                    return (a.avgWaitTime ?? Infinity) - (b.avgWaitTime ?? Infinity);
                case 'qubits':
                    return b.qubits - a.qubits;
                case 'performance':
                    return (b.performanceScore ?? -1) - (a.performanceScore ?? -1);
                default:
                    return 0;
            }
        });
        
        this.displayComparisonTable(filteredData);
    }

    displayComparisonTable(backends) {
        const tbody = document.getElementById('comparison-tbody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        backends.forEach(backend => {
            const row = document.createElement('tr');
            row.className = `backend-row ${backend.status}`;
            
            const recommendation = this.getRecommendation(backend);
            const avgWaitTime = this.formatWaitTime(backend.avgWaitTime);
            
            row.innerHTML = `
                <td class="backend-name">
                    <div class="backend-info">
                        <strong>${backend.name}</strong>
                        <span class="backend-type">Hardware</span>
                    </div>
                </td>
                <td class="status-cell">
                    <span class="status-indicator ${backend.status}"></span>
                    <span class="status-text">${backend.status}</span>
                </td>
                <td class="qubits-cell">
                    <span class="qubit-count">${backend.qubits}</span>
                    <span class="qubit-label">qubits</span>
                </td>
                <td class="queue-cell">
                    <div class="queue-info">
                        <span class="queue-count ${this.getQueueClass(backend.queue)}">${backend.queue}</span>
                        <div class="queue-trend">${this.getQueueTrend(backend.name)}</div>
                    </div>
                </td>
                <td class="execution-time-cell">
                    <span class="execution-time">${backend.avgExecutionTime ? backend.avgExecutionTime.toFixed(1) + 's' : '—'}</span>
                </td>
                <td class="success-rate-cell">
                    <div class="success-rate">
                        <span class="rate-value">${backend.successRate || 0}%</span>
                        <div class="rate-bar">
                            <div class="rate-fill" style="width: ${backend.successRate || 0}%"></div>
                        </div>
                    </div>
                </td>
                <td class="fidelity-cell">
                    <div class="fidelity-info">
                        <span class="fidelity-value">${backend.avgFidelity || 0}%</span>
                        <div class="fidelity-bar">
                            <div class="fidelity-fill" style="width: ${backend.avgFidelity || 0}%"></div>
                        </div>
                    </div>
                </td>
                <td class="calibration-cell">
                    <div class="calibration-info">
                        <span class="calibration-status ${backend.calibrationStatus}">${backend.calibrationStatus}</span>
                        <span class="calibration-quality">${backend.calibrationQuality || 0}%</span>
                    </div>
                </td>
                <td class="gate-error-cell">
                    <span class="gate-error">${backend.gateErrorRate ? (backend.gateErrorRate * 100).toFixed(3) + '%' : '—'}</span>
                </td>
                <td class="coherence-cell">
                    <span class="coherence-time">${backend.coherenceTime ? (backend.coherenceTime / 1000).toFixed(1) + 'μs' : '—'}</span>
                </td>
                <td class="usage-cell">
                    <span class="usage-count">${backend.usageCount || 0}</span>
                    <span class="usage-label">jobs</span>
                </td>
                <td class="recommendation-cell">
                    <span class="recommendation ${recommendation.type}" title="${backend.explanation || ''}">
                        <i class="fas fa-${recommendation.icon}"></i>
                        ${recommendation.text}
                    </span>
                </td>
            `;
            
            tbody.appendChild(row);
        });
    }

    getRecommendation(backend) {
        if (backend.status !== 'online') {
            return { type: 'poor', icon: 'ban', text: 'Unavailable' };
        }
        if (backend.recommendationRank === 1) {
            return { type: 'excellent', icon: 'star', text: 'Best Choice' };
        }
        if (backend.recommendationRank && backend.recommendationRank <= 3) {
            return { type: 'good', icon: 'thumbs-up', text: 'Recommended' };
        }
        if ((backend.avgWaitTime ?? Infinity) <= 300) {
            return { type: 'good', icon: 'thumbs-up', text: 'Low Wait' };
        }
        if (backend.queue <= 5) {
            return { type: 'moderate', icon: 'clock', text: 'Moderate Wait' };
        }
        return { type: 'poor', icon: 'exclamation-triangle', text: 'Long Wait' };
    }

    getQueueClass(queue) {
        if (queue === 0) return 'queue-empty';
        if (queue <= 2) return 'queue-low';
        if (queue <= 5) return 'queue-medium';
        return 'queue-high';
    }

    getQueueTrend(backendName) {
        const history = this.queueHistory.get(backendName);
        if (!history || history.length < 2) return '';
        
        const recent = history.slice(-5);
        const trend = recent[recent.length - 1].queue - recent[0].queue;
        
        if (trend > 0) return '<i class="fas fa-arrow-up trend-up"></i>';
        if (trend < 0) return '<i class="fas fa-arrow-down trend-down"></i>';
        return '<i class="fas fa-minus trend-stable"></i>';
    }

    formatWaitTime(seconds) {
        if (seconds < 60) return `${seconds}s`;
        if (seconds < 3600) return `${Math.round(seconds / 60)}m`;
        return `${Math.round(seconds / 3600)}h`;
    }

    generateInsights() {
        const insightsContent = document.getElementById('insights-content');
        if (!insightsContent) return;
        
        const insights = this.analyzeBackendData();
        const algo = document.getElementById('algo-option')?.value || 'auto';
        const complexity = document.getElementById('complexity-option')?.value || 'medium';
        insightsContent.innerHTML = insights.map(insight => `
            <div class="insight-item ${insight.type}">
                <i class="fas fa-${insight.icon}"></i>
                <div class="insight-content">
                    <h4>${insight.title}</h4>
                    <p>${insight.description}</p>
                </div>
            </div>
        `).join('') + `
            <div class="insight-item info">
                <i class="fas fa-sliders-h"></i>
                <div class="insight-content">
                    <h4>Recommendation Settings</h4>
                    <p>Algorithm: <strong>${algo}</strong>, Complexity: <strong>${complexity}</strong></p>
                </div>
            </div>
        `;
    }

    analyzeBackendData() {
        const insights = [];
        const backends = Array.from(this.backends.values());
        
        // Check if we have any backends
        if (backends.length === 0) {
            console.log('No backends available for analysis');
            return insights;
        }
        
        // Find best performing backend
        const bestBackend = backends.reduce((best, current) => 
            current.performanceScore > best.performanceScore ? current : best
        );
        
        insights.push({
            type: 'success',
            icon: 'trophy',
            title: 'Best Performing Backend',
            description: `${bestBackend.name} has the highest performance score (${bestBackend.performanceScore}) with ${bestBackend.queue} jobs in queue.`
        });
        
        // Find backends with no queue
        const availableBackends = backends.filter(b => b.queue === 0 && b.status === 'online');
        if (availableBackends.length > 0) {
            insights.push({
                type: 'info',
                icon: 'check-circle',
                title: 'Available Backends',
                description: `${availableBackends.length} backend(s) are currently available with no queue: ${availableBackends.map(b => b.name).join(', ')}.`
            });
        }
        
        // Check for high queue backends
        const highQueueBackends = backends.filter(b => b.queue > 5);
        if (highQueueBackends.length > 0) {
            insights.push({
                type: 'warning',
                icon: 'exclamation-triangle',
                title: 'High Queue Alert',
                description: `${highQueueBackends.length} backend(s) have long queues: ${highQueueBackends.map(b => `${b.name} (${b.queue})`).join(', ')}.`
            });
        }
        
        // Performance trend analysis
        const avgPerformance = backends.reduce((sum, b) => sum + b.performanceScore, 0) / backends.length;
        insights.push({
            type: 'info',
            icon: 'chart-line',
            title: 'System Performance',
            description: `Average system performance is ${avgPerformance.toFixed(1)}%. ${avgPerformance > 80 ? 'System is performing well.' : 'Consider optimizing job distribution.'}`
        });
        
        return insights;
    }

    showComparisonModal() {
        const modal = document.getElementById('backend-comparison-modal');
        if (modal) {
            modal.classList.add('active');
            this.refreshComparisonData();
        }
    }

    closeComparisonModal() {
        const modal = document.getElementById('backend-comparison-modal');
        if (modal) {
            modal.classList.remove('active');
        }
    }

    refreshComparisonData() {
        this.collectBackendData();
        this.showNotification('Backend data refreshed', 'info');
    }

    showNotification(message, type = 'info') {
        if (window.enhancedNotifications) {
            window.enhancedNotifications.showNotification('Backend Comparison', message, type);
        }
    }

    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
    }
}

// Initialize backend comparison system
document.addEventListener('DOMContentLoaded', () => {
    window.backendComparison = new BackendComparisonSystem();
});