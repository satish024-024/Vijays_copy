// Enhanced AI Assistant for Quantum Jobs Tracker
// Comprehensive quantum computing knowledge and dashboard integration
class EnhancedQuantumAI {
    constructor(dashboard) {
        this.dashboard = dashboard;
        this.quantumKnowledge = this.initializeQuantumKnowledge();
        this.projectInfo = this.initializeProjectInfo();
        this.apiEndpoints = this.initializeAPIEndpoints();
        this.widgetCapabilities = this.initializeWidgetCapabilities();
        this.conversationHistory = [];
        this.maxHistoryLength = 50;
    }

    initializeQuantumKnowledge() {
        return {
            fundamental: {
                superposition: "A quantum state can exist in multiple states simultaneously until measured. |ψ⟩ = α|0⟩ + β|1⟩ where α and β are complex amplitudes.",
                entanglement: "Quantum particles can be correlated such that the state of one instantly affects the other, regardless of distance. Enables quantum teleportation and superdense coding.",
                interference: "Quantum amplitudes can interfere constructively or destructively, enabling quantum algorithms like Grover's search.",
                measurement: "Observing a quantum system collapses its superposition to a classical outcome, following the Born rule |α|²."
            },

            gates: {
                hadamard: "H gate creates superposition: H|0⟩ = (|0⟩ + |1⟩)/√2, H|1⟩ = (|0⟩ - |1⟩)/√2",
                pauli_x: "X gate (NOT): X|0⟩ = |1⟩, X|1⟩ = |0⟩. Flips qubit state.",
                pauli_y: "Y gate: Y|0⟩ = i|1⟩, Y|1⟩ = -i|0⟩. Rotation around Y-axis by π.",
                pauli_z: "Z gate: Z|0⟩ = |0⟩, Z|1⟩ = -|1⟩. Phase flip gate.",
                cnot: "Controlled-NOT: Flips target qubit if control is |1⟩. Creates entanglement.",
                rotation: "Rx(θ), Ry(θ), Rz(θ): Rotate qubit state by angle θ around respective axes.",
                phase: "S gate: Z^(1/2), T gate: Z^(1/4). Add phases to |1⟩ state."
            },

            algorithms: {
                shor: "Factorizes large numbers exponentially faster than classical computers using quantum Fourier transform.",
                grover: "Searches unsorted databases quadratically faster using amplitude amplification.",
                deutsch_jozsa: "Determines if a function is constant or balanced with single evaluation.",
                quantum_walk: "Quantum version of random walk, useful for search algorithms.",
                hhl: "Solves linear systems of equations exponentially faster than classical methods."
            },

            hardware: {
                qubits: "Basic quantum information units. Can be implemented as superconducting circuits, trapped ions, photons, etc.",
                coherence: "T1 (amplitude damping) and T2 (phase damping) times determine how long quantum information persists.",
                gate_errors: "Imperfections in quantum gate operations, measured as infidelity from ideal unitary.",
                readout_errors: "Errors in measuring qubit states, affect measurement accuracy.",
                crosstalk: "Unwanted interactions between qubits, can cause correlated errors."
            },

            noise_models: {
                depolarizing: "Each qubit has probability p of being replaced by completely mixed state.",
                amplitude_damping: "Energy relaxation: |1⟩ → |0⟩ with rate γ.",
                phase_damping: "Loss of quantum phase information without energy loss.",
                coherent_errors: "Systematic errors that preserve quantum coherence.",
                incoherent_errors: "Random errors that destroy quantum coherence."
            },

            quantum_advantage: {
                simulation: "Quantum systems can efficiently simulate other quantum systems (quantum supremacy achieved 2019).",
                optimization: "Quantum algorithms for optimization problems (QAOA, VQE).",
                machine_learning: "Quantum machine learning algorithms with potential exponential speedup.",
                cryptography: "Quantum-resistant cryptography and quantum key distribution.",
                chemistry: "Molecular simulation for drug discovery and materials science."
            }
        };
    }

    initializeProjectInfo() {
        return {
            name: "Quantum Jobs Tracker",
            version: "2.0.0",
            description: "Advanced quantum computing job monitoring and analysis platform",
            features: [
                "Real-time IBM Quantum backend monitoring",
                "Comprehensive job tracking and analysis",
                "Performance metrics and optimization",
                "Calibration status monitoring",
                "Circuit visualization and analysis",
                "Historical data analysis",
                "Multi-theme dashboard interface",
                "AI-powered quantum assistant"
            ],
            technologies: [
                "Flask (Python backend)",
                "IBM Quantum Runtime Service",
                "Three.js (3D visualizations)",
                "Chart.js (data visualization)",
                "WebSocket/SSE (real-time updates)",
                "Google Gemini AI integration"
            ],
            apis: [
                "IBM Quantum Runtime API",
                "IBM Quantum Backend Properties API",
                "IBM Quantum Jobs API",
                "IBM Quantum Calibration API",
                "IBM Quantum Performance API"
            ],
            dashboards: [
                "Hackathon Dashboard - Educational quantum learning",
                "Modern Dashboard - Clean predictive analytics",
                "Professional Dashboard - Enterprise-grade monitoring",
                "Advanced Dashboard - Technical scientific interface"
            ],
            capabilities: [
                "Monitor 100+ quantum backends worldwide",
                "Track millions of quantum jobs",
                "Analyze quantum circuit performance",
                "Predict execution times and queue positions",
                "Monitor calibration quality and system health",
                "Provide quantum computing education",
                "Optimize quantum job scheduling"
            ]
        };
    }

    initializeAPIEndpoints() {
        return {
            backends: {
                endpoint: '/api/backends',
                description: 'Get detailed information about all available IBM Quantum backends',
                data: ['name', 'status', 'qubits', 'gate_errors', 'readout_errors', 't1_times', 't2_times', 'coupling_map', 'basis_gates']
            },
            jobs: {
                endpoint: '/api/jobs',
                description: 'Retrieve quantum job information and status',
                data: ['job_id', 'backend', 'status', 'shots', 'created_time']
            },
            job_results: {
                endpoint: '/api/job_results',
                description: 'Get actual quantum measurement results and execution data',
                data: ['measurements', 'fidelity', 'execution_time', 'circuits']
            },
            performance: {
                endpoint: '/api/performance_metrics',
                description: 'Comprehensive performance analytics and metrics',
                data: ['success_rate', 'execution_times', 'queue_times', 'fidelity_scores', 'backend_performance']
            },
            realtime: {
                endpoint: '/api/realtime_monitoring',
                description: 'Live queue positions and system status',
                data: ['queue_status', 'system_status', 'estimated_wait_times']
            },
            calibration: {
                endpoint: '/api/calibration_data',
                description: 'Backend calibration status and system health',
                data: ['calibration_status', 'calibration_quality', 'system_health', 'backend_calibrations']
            },
            historical: {
                endpoint: '/api/historical_data',
                description: 'Historical performance trends and usage patterns',
                data: ['success_trend', 'performance_trend', 'backend_usage', 'error_patterns']
            },
            circuit_details: {
                endpoint: '/api/circuit_details',
                description: 'Quantum circuit analysis and gate information',
                data: ['gates', 'depth', 'qubit_mapping', 'transpilation_info']
            },
            dashboard_metrics: {
                endpoint: '/api/dashboard_metrics',
                description: 'Aggregated dashboard metrics for overview',
                data: ['active_backends', 'total_jobs', 'running_jobs', 'success_rate']
            }
        };
    }

    initializeWidgetCapabilities() {
        return {
            backends: {
                name: 'Quantum Backends',
                capabilities: ['View backend status', 'Compare performance', 'Monitor calibration', 'Analyze gate errors'],
                interactions: ['Refresh data', 'Filter backends', 'Sort by metrics', 'View detailed properties']
            },
            jobs: {
                name: 'Active Jobs',
                capabilities: ['Monitor job status', 'View execution progress', 'Track queue positions', 'Analyze completion rates'],
                interactions: ['Cancel jobs', 'View job details', 'Export results', 'Filter by status']
            },
            bloch_sphere: {
                name: '3D Bloch Sphere',
                capabilities: ['Visualize quantum states', 'Interactive rotation', 'State evolution', 'Measurement simulation'],
                interactions: ['Apply quantum gates', 'Reset state', 'Export visualization', 'Toggle history']
            },
            circuit: {
                name: '3D Quantum Circuit',
                capabilities: ['Circuit visualization', 'Gate sequence', 'Qubit mapping', 'Step-by-step execution'],
                interactions: ['Play/pause animation', 'Step through gates', 'Reset circuit', 'Expand view']
            },
            performance: {
                name: 'Performance Analytics',
                capabilities: ['Execution time analysis', 'Success rate tracking', 'Fidelity monitoring', 'Trend analysis'],
                interactions: ['Filter time range', 'Compare backends', 'Export metrics', 'View detailed charts']
            },
            entanglement: {
                name: 'Entanglement Analysis',
                capabilities: ['Correlation analysis', 'Bell state visualization', 'Entanglement entropy', 'Measurement correlations'],
                interactions: ['Generate entangled states', 'Measure correlations', 'Calculate entropy', 'Export data']
            },
            results: {
                name: 'Measurement Results',
                capabilities: ['View quantum measurements', 'Probability distributions', 'Error analysis', 'Statistical analysis'],
                interactions: ['Filter results', 'Export data', 'Compare experiments', 'Statistical tests']
            },
            quantum_state: {
                name: 'Quantum State',
                capabilities: ['State vector display', 'Density matrix', 'Purity calculation', 'State tomography'],
                interactions: ['Apply operations', 'Calculate observables', 'Export state', 'Reset to |0⟩']
            },
            ai_chat: {
                name: 'AI Quantum Assistant',
                capabilities: ['Quantum education', 'Code generation', 'Problem solving', 'System analysis'],
                interactions: ['Ask questions', 'Get explanations', 'Request code', 'System recommendations']
            }
        };
    }

    async processQuery(query) {
        const lowerQuery = query.toLowerCase();
        this.addToHistory(query, 'user');

        // Check for widget interactions
        const widgetInteraction = this.checkWidgetInteraction(lowerQuery);
        if (widgetInteraction) {
            return widgetInteraction;
        }

        // Check for API queries
        const apiQuery = this.checkAPIQuery(lowerQuery);
        if (apiQuery) {
            return apiQuery;
        }

        // Check for quantum knowledge queries
        const knowledgeQuery = this.checkQuantumKnowledge(lowerQuery);
        if (knowledgeQuery) {
            return knowledgeQuery;
        }

        // Check for project information queries
        const projectQuery = this.checkProjectInfo(lowerQuery);
        if (projectQuery) {
            return projectQuery;
        }

        // Check for system analysis queries
        const systemQuery = this.checkSystemAnalysis(lowerQuery);
        if (systemQuery) {
            return systemQuery;
        }

        // Default response with comprehensive help
        return this.generateHelpfulResponse(lowerQuery);
    }

    checkWidgetInteraction(query) {
        const widgets = this.widgetCapabilities;

        // Check for specific widget requests
        for (const [widgetKey, widgetInfo] of Object.entries(widgets)) {
            if (query.includes(widgetKey) || query.includes(widgetInfo.name.toLowerCase())) {
                if (query.includes('show') || query.includes('open') || query.includes('view')) {
                    // Actually open the widget
                    if (this.dashboard && typeof this.dashboard.openWidget === 'function') {
                        const result = this.dashboard.openWidget(widgetKey);
                        return `${result} ${widgetInfo.capabilities.join('. ')}`;
                    }
                    return `Opening ${widgetInfo.name} widget. ${widgetInfo.capabilities.join('. ')}`;
                }
                if (query.includes('help') || query.includes('what can')) {
                    return `${widgetInfo.name} can: ${widgetInfo.capabilities.join(', ')}. Interactions: ${widgetInfo.interactions.join(', ')}.`;
                }
                if (query.includes('refresh') || query.includes('update')) {
                    // Actually refresh the widget
                    if (this.dashboard && typeof this.dashboard.refreshWidget === 'function') {
                        const result = this.dashboard.refreshWidget(widgetKey);
                        return result;
                    }
                    return `Refreshing ${widgetInfo.name} with latest data...`;
                }
                if (query.includes('reset') || query.includes('clear')) {
                    return `Resetting ${widgetInfo.name} to default state...`;
                }
            }
        }

        // Check for general widget operations
        if (query.includes('refresh') || query.includes('update')) {
            return 'Refreshing all widgets with latest IBM Quantum data...';
        }

        if (query.includes('reset') || query.includes('clear')) {
            return 'Resetting widgets to default state...';
        }

        return null;
    }

    checkAPIQuery(query) {
        const apis = this.apiEndpoints;

        for (const [apiKey, apiInfo] of Object.entries(apis)) {
            if (query.includes(apiKey) || query.includes(apiInfo.endpoint.split('/').pop())) {
                if (query.includes('data') || query.includes('info') || query.includes('get')) {
                    return `API ${apiInfo.endpoint}: ${apiInfo.description}. Provides: ${apiInfo.data.join(', ')}.`;
                }
                if (query.includes('status') || query.includes('health')) {
                    return `API ${apiInfo.endpoint} is active and providing real-time IBM Quantum data.`;
                }
            }
        }

        if (query.includes('api') && query.includes('list')) {
            const apiList = Object.entries(apis).map(([key, info]) =>
                `${key}: ${info.endpoint} - ${info.description}`
            ).join('\n');
            return `Available APIs:\n${apiList}`;
        }

        return null;
    }

    checkQuantumKnowledge(query) {
        const knowledge = this.quantumKnowledge;

        // Check fundamental concepts
        for (const [concept, explanation] of Object.entries(knowledge.fundamental)) {
            if (query.includes(concept)) {
                return `${concept.charAt(0).toUpperCase() + concept.slice(1)}: ${explanation}`;
            }
        }

        // Check quantum gates
        for (const [gate, explanation] of Object.entries(knowledge.gates)) {
            if (query.includes(gate) || query.includes(gate.replace('_', ' '))) {
                return `${gate.toUpperCase()} Gate: ${explanation}`;
            }
        }

        // Check algorithms
        for (const [algorithm, explanation] of Object.entries(knowledge.algorithms)) {
            if (query.includes(algorithm)) {
                return `${algorithm.toUpperCase()}: ${explanation}`;
            }
        }

        // Check hardware concepts
        for (const [topic, explanation] of Object.entries(knowledge.hardware)) {
            if (query.includes(topic)) {
                return `${topic.charAt(0).toUpperCase() + topic.slice(1)}: ${explanation}`;
            }
        }

        // Check noise models
        for (const [model, explanation] of Object.entries(knowledge.noise_models)) {
            if (query.includes(model) || query.includes('noise')) {
                return `${model.charAt(0).toUpperCase() + model.slice(1)} Noise: ${explanation}`;
            }
        }

        // Check quantum advantage
        for (const [area, explanation] of Object.entries(knowledge.quantum_advantage)) {
            if (query.includes(area) || query.includes('advantage')) {
                return `Quantum Advantage in ${area.charAt(0).toUpperCase() + area.slice(1)}: ${explanation}`;
            }
        }

        return null;
    }

    checkProjectInfo(query) {
        const project = this.projectInfo;

        if (query.includes('project') || query.includes('system')) {
            if (query.includes('name') || query.includes('what is')) {
                return `${project.name} v${project.version}: ${project.description}`;
            }
            if (query.includes('features') || query.includes('capabilities')) {
                return `Key Features: ${project.features.join(', ')}`;
            }
            if (query.includes('technologies') || query.includes('tech')) {
                return `Technologies: ${project.technologies.join(', ')}`;
            }
            if (query.includes('apis') || query.includes('endpoints')) {
                return `APIs: ${project.apis.join(', ')}`;
            }
            if (query.includes('dashboards') || query.includes('themes')) {
                return `Dashboards: ${project.dashboards.join(', ')}`;
            }
        }

        if (query.includes('version') || query.includes('v2')) {
            return `Current version: ${project.version}. This includes enhanced IBM Quantum integration, comprehensive AI capabilities, and multi-theme dashboards.`;
        }

        return null;
    }

    checkSystemAnalysis(query) {
        if (!this.dashboard?.state) return null;

        const state = this.dashboard.state;

        if (query.includes('status') || query.includes('health')) {
            return `System Status: ${state.isConnected ? 'Connected' : 'Disconnected'} to IBM Quantum. ` +
                   `${state.backends?.length || 0} backends available, ` +
                   `${state.jobs?.length || 0} jobs tracked. ` +
                   `Success rate: ${this.dashboard.calculateEnhancedSuccessRate()}%.`;
        }

        if (query.includes('performance') || query.includes('metrics')) {
            const perf = state.performance;
            if (perf) {
                return `Performance Metrics: Avg execution time ${perf.average_execution_time?.toFixed(2)}s, ` +
                       `Success rate ${(perf.success_rate * 100)?.toFixed(1)}%, ` +
                       `Fidelity ${(perf.average_fidelity * 100)?.toFixed(1)}%. ` +
                       `Total jobs analyzed: ${state.historical?.total_jobs || 0}.`;
            }
        }

        if (query.includes('backends') || query.includes('backend')) {
            const backends = state.backends || [];
            const operational = backends.filter(b => b.operational).length;
            return `Backend Analysis: ${operational}/${backends.length} backends operational. ` +
                   `Total qubits: ${backends.reduce((sum, b) => sum + (b.num_qubits || 0), 0)}. ` +
                   `Calibration status: ${state.calibration?.calibration_status || 'Unknown'}.`;
        }

        if (query.includes('jobs') || query.includes('queue')) {
            const realtime = state.realtime;
            if (realtime) {
                return `Queue Status: ${realtime.system_status?.total_pending_jobs || 0} jobs pending, ` +
                       `Average wait time: ${realtime.system_status?.average_queue_time?.toFixed(0) || 'N/A'}s. ` +
                       `System load: ${realtime.system_status?.total_active_backends || 0} active backends.`;
            }
        }

        if (query.includes('calibration') || query.includes('quality')) {
            const calib = state.calibration;
            if (calib) {
                return `Calibration Status: ${calib.calibration_status}, ` +
                       `System health: ${calib.system_health?.overall_status}, ` +
                       `Quality score: ${(Object.values(calib.backend_calibrations || {}).reduce((sum, b) => sum + (b.calibration_quality || 0), 0) / Object.keys(calib.backend_calibrations || {}).length)?.toFixed(1) || 'N/A'}%.`;
            }
        }

        return null;
    }

    generateHelpfulResponse(query) {
        const theme = this.dashboard?.dashboardTheme || 'Quantum';

        // Check for greetings
        if (query.includes('hello') || query.includes('hi') || query.includes('hey')) {
            return `Hello! I'm your ${theme} Quantum AI Assistant. I have access to comprehensive IBM Quantum data, all dashboard widgets, and extensive quantum computing knowledge. How can I help you today?`;
        }

        // Check for help requests
        if (query.includes('help') || query.includes('what can you') || query.includes('commands')) {
            return `I can help you with:
• 📊 **System Analysis**: Check backend status, performance metrics, queue positions
• 🎯 **Widget Control**: Open, refresh, or interact with any dashboard widget
• 🔬 **Quantum Knowledge**: Explain concepts, gates, algorithms, and hardware
• 📈 **Data Analysis**: Access all IBM Quantum APIs and analyze results
• 🤖 **AI Features**: Generate quantum code, solve problems, provide recommendations
• 📋 **Project Info**: Learn about Quantum Jobs Tracker capabilities

Try asking: "Show me backend performance", "Explain quantum entanglement", "What's the current queue status?", or "Open Bloch sphere widget".`;
        }

        // Check for general questions about capabilities
        if (query.includes('can you') || query.includes('do you')) {
            return `Yes, I can:
• Access and analyze all IBM Quantum backend data
• Control and interact with all dashboard widgets
• Provide detailed quantum computing explanations
• Monitor system performance and calibration status
• Generate insights from historical data
• Help optimize quantum job scheduling
• Answer questions about the Quantum Jobs Tracker project

What specific task would you like me to help with?`;
        }

        // Default fallback with context
        const capabilities = [
            'analyze quantum backends and their performance',
            'explain quantum computing concepts and algorithms',
            'monitor job queues and execution times',
            'provide system health and calibration status',
            'control dashboard widgets and visualizations',
            'access real-time IBM Quantum data',
            'generate quantum circuit insights',
            'optimize quantum job scheduling'
        ];

        return `I'm your advanced ${theme} Quantum AI Assistant with comprehensive capabilities. I can ${capabilities.slice(0, 4).join(', ')}, and ${capabilities.slice(4).join(', ')}.

Try asking me about:
• "What's the current system status?"
• "Explain quantum superposition"
• "Show me backend performance data"
• "Open the Bloch sphere widget"
• "What are the latest job results?"

How can I assist you with quantum computing today?`;
    }

    addToHistory(message, type) {
        this.conversationHistory.push({
            message,
            type,
            timestamp: Date.now()
        });

        // Keep only recent history
        if (this.conversationHistory.length > this.maxHistoryLength) {
            this.conversationHistory = this.conversationHistory.slice(-this.maxHistoryLength);
        }
    }

    getConversationHistory() {
        return this.conversationHistory;
    }

    clearHistory() {
        this.conversationHistory = [];
        return 'Conversation history cleared.';
    }

    // Method to get comprehensive system overview
    getSystemOverview() {
        if (!this.dashboard?.state) return 'Dashboard not initialized.';

        const state = this.dashboard.state;
        const backends = state.backends || [];
        const jobs = state.jobs || [];

        return {
            connection: state.isConnected ? 'Connected to IBM Quantum' : 'Disconnected',
            backends: {
                total: backends.length,
                operational: backends.filter(b => b.operational).length,
                totalQubits: backends.reduce((sum, b) => sum + (b.num_qubits || 0), 0)
            },
            jobs: {
                total: jobs.length,
                running: jobs.filter(j => j.status === 'running').length,
                completed: jobs.filter(j => j.status === 'completed').length
            },
            performance: {
                successRate: this.dashboard.calculateEnhancedSuccessRate(),
                avgExecutionTime: state.performance?.average_execution_time,
                avgFidelity: state.performance?.average_fidelity
            },
            calibration: {
                status: state.calibration?.calibration_status,
                health: state.calibration?.system_health?.overall_status
            }
        };
    }

    // Method to generate quantum code examples
    generateQuantumCode(request) {
        if (request.includes('bell') || request.includes('entanglement')) {
            return `from qiskit import QuantumCircuit

# Create Bell state (entangled qubits)
qc = QuantumCircuit(2, 2)
qc.h(0)        # Put first qubit in superposition
qc.cx(0, 1)    # Entangle qubits with CNOT gate
qc.measure_all() # Measure both qubits

print("Bell State Circuit:")
print(qc.draw())`;
        }

        if (request.includes('grover') || request.includes('search')) {
            return `from qiskit import QuantumCircuit
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.utils import QuantumInstance

# Grover's algorithm for searching marked items
def grover_search(search_value, search_space):
    # This is a simplified example
    # In practice, you'd implement the oracle and diffuser
    qc = QuantumCircuit(4)  # 2^4 = 16 possible values

    # Initialize superposition
    qc.h(range(4))

    # Oracle (marks the search value)
    # This would be customized based on the search problem

    # Diffuser (amplitude amplification)
    qc.h(range(4))
    qc.x(range(4))
    qc.h(3)
    qc.mct([0,1,2], 3)  # Multi-controlled Toffoli
    qc.h(3)
    qc.x(range(4))
    qc.h(range(4))

    return qc`;
        }

        if (request.includes('teleportation')) {
            return `from qiskit import QuantumCircuit

# Quantum Teleportation Protocol
def quantum_teleportation():
    qc = QuantumCircuit(3, 3)

    # Step 1: Create entangled pair (Bell state)
    qc.h(1)
    qc.cx(1, 2)

    # Step 2: Prepare qubit to teleport (arbitrary state)
    qc.h(0)  # Example: put qubit 0 in superposition

    # Step 3: Bell measurement on qubits 0 and 1
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])

    # Step 4: Classical communication and conditional operations
    qc.x(2).c_if(1, 1)  # Apply X if classical bit 1 is 1
    qc.z(2).c_if(0, 1)  # Apply Z if classical bit 0 is 1

    qc.measure(2, 2)  # Measure teleported qubit

    return qc

print("Quantum Teleportation Circuit:")
print(quantum_teleportation().draw())`;
        }

        return `I can generate quantum code examples! Try asking for:
• "Generate Bell state code"
• "Show Grover search algorithm"
• "Create quantum teleportation circuit"
• "Generate VQE algorithm code"`;
    }
}

// Make EnhancedQuantumAI globally available
window.EnhancedQuantumAI = EnhancedQuantumAI;
