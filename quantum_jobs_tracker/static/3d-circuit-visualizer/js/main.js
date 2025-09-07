// 3D Quantum Circuit Visualizer - Main Application Entry Point
// Main application controller and initialization

class QuantumVisualizerApp {
    constructor() {
        this.quantumVisualizer = null;
        this.quantumCircuit = null;
        this.ibmIntegration = null;
        this.currentCircuit = null;
        this.isInitialized = false;

        this.init();
    }

    async init() {
        try {
            // Show loading screen
            this.showLoadingScreen();

            // Initialize components
            await this.initializeComponents();

            // Setup event listeners
            this.setupEventListeners();

            // Hide loading screen
            this.hideLoadingScreen();

            this.isInitialized = true;
            console.log('Quantum Visualizer initialized successfully');
        } catch (error) {
            console.error('Failed to initialize Quantum Visualizer:', error);
            this.showError('Failed to initialize application');
        }
    }

    showLoadingScreen() {
        const loadingScreen = document.getElementById('loading-screen');
        loadingScreen.classList.remove('hidden');
    }

    hideLoadingScreen() {
        const loadingScreen = document.getElementById('loading-screen');
        const app = document.getElementById('app');

        setTimeout(() => {
            loadingScreen.classList.add('fade-out');
            app.classList.remove('hidden');

            setTimeout(() => {
                loadingScreen.classList.add('hidden');
                loadingScreen.classList.remove('fade-out');
            }, 500);
        }, 1000);
    }

    async initializeComponents() {
        console.log('🚀 Starting component initialization...');

        // Step 1: Check Three.js
        console.log('Step 1: Checking Three.js...');
        if (typeof THREE === 'undefined') {
            console.log('⚠️ Three.js not found, attempting to load locally...');

            // Try to load local Three.js if available
            try {
                await new Promise((resolve, reject) => {
                    const script = document.createElement('script');
                    script.src = 'three.min.js'; // Local copy if available
                    script.onload = () => {
                        console.log('✅ Three.js loaded from local file');
                        resolve();
                    };
                    script.onerror = () => {
                        reject(new Error('Three.js not available locally'));
                    };
                    document.head.appendChild(script);
                });
            } catch (localError) {
                throw new Error('Three.js library not loaded. Please check your internet connection and reload the page. You can also download Three.js locally.');
            }
        }
        console.log('✅ Three.js loaded (v' + THREE.REVISION + ')');

        // Step 2: Check canvas element
        console.log('Step 2: Checking canvas element...');
        const canvasElement = document.getElementById('threejs-canvas');
        if (!canvasElement) {
            throw new Error('Canvas element not found. Please check the HTML structure.');
        }
        console.log('✅ Canvas element found:', canvasElement);
        console.log('Canvas dimensions:', canvasElement.clientWidth, 'x', canvasElement.clientHeight);

        // Step 3: Test WebGL before initializing
        console.log('Step 3: Testing WebGL...');
        const testCanvas = document.createElement('canvas');
        const gl = testCanvas.getContext('webgl') || testCanvas.getContext('experimental-webgl');
        if (!gl) {
            throw new Error('WebGL not supported. Please enable WebGL in your browser settings.');
        }
        console.log('✅ WebGL supported');

        // Step 4: Initialize Three.js visualizer
        console.log('Step 4: Initializing Three.js visualizer...');
        try {
            this.quantumVisualizer = new QuantumVisualizer('threejs-canvas');
            console.log('✅ QuantumVisualizer initialized');
        } catch (error) {
            console.error('❌ QuantumVisualizer initialization failed:', error);
            throw error;
        }

        // Step 5: Initialize quantum circuit (optional - can fail gracefully)
        console.log('Step 5: Initializing quantum circuit logic...');
        try {
            this.quantumCircuit = new QuantumCircuit();
            console.log('✅ QuantumCircuit initialized');
        } catch (error) {
            console.warn('⚠️ QuantumCircuit initialization failed, continuing:', error);
            this.quantumCircuit = null;
        }

        // Step 6: Initialize IBM integration (optional)
        console.log('Step 6: Initializing IBM integration...');
        try {
            this.ibmIntegration = new IBMIntegration();
            console.log('✅ IBM integration initialized');
        } catch (error) {
            console.warn('⚠️ IBM integration initialization failed, continuing:', error);
            this.ibmIntegration = null;
        }

        // Step 7: Create initial circuit (only if QuantumCircuit is available)
        if (this.quantumCircuit) {
            console.log('Step 7: Creating initial circuit...');
            try {
                this.currentCircuit = this.quantumCircuit.createCircuit(2);
                console.log('✅ Initial circuit created');
            } catch (error) {
                console.warn('⚠️ Circuit creation failed, continuing:', error);
                this.currentCircuit = null;
            }
        }

        // Step 8: Update UI
        console.log('Step 8: Updating UI...');
        this.updateCircuitInfo();

        console.log('🎉 Components initialized successfully');
    }

    setupEventListeners() {
        // Navigation buttons
        document.getElementById('new-circuit').addEventListener('click', () => this.newCircuit());
        document.getElementById('load-circuit').addEventListener('click', () => this.loadCircuit());
        document.getElementById('save-circuit').addEventListener('click', () => this.saveCircuit());
        document.getElementById('ibm-connect').addEventListener('click', () => this.showIBMModal());

        // Circuit controls
        document.getElementById('play-btn').addEventListener('click', () => this.playCircuit());
        document.getElementById('pause-btn').addEventListener('click', () => this.pauseCircuit());
        document.getElementById('reset-btn').addEventListener('click', () => this.resetCircuit());
        document.getElementById('add-qubit').addEventListener('click', () => this.addQubit());
        document.getElementById('remove-qubit').addEventListener('click', () => this.removeQubit());

        // Scene controls
        document.getElementById('reset-camera').addEventListener('click', () => this.resetCamera());
        document.getElementById('toggle-grid').addEventListener('click', () => this.toggleGrid());
        document.getElementById('toggle-axes').addEventListener('click', () => this.toggleAxes());

        // Gate palette
        this.setupGatePalette();

        // IBM modal
        document.getElementById('ibm-modal-close').addEventListener('click', () => this.hideIBMModal());
        document.getElementById('ibm-connect-btn').addEventListener('click', () => this.connectIBM());

        // Console
        document.getElementById('clear-console').addEventListener('click', () => this.clearConsole());

        // Sidebar collapse
        document.getElementById('gate-collapse').addEventListener('click', () => this.toggleSidebar('left'));
        document.getElementById('properties-collapse').addEventListener('click', () => this.toggleSidebar('right'));
    }

    setupGatePalette() {
        const gateItems = document.querySelectorAll('.gate-item');

        gateItems.forEach(item => {
            item.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', item.dataset.gate);
                item.classList.add('dragging');
            });

            item.addEventListener('dragend', () => {
                item.classList.remove('dragging');
            });
        });

        // Setup drop zones for circuit positions
        const canvas = document.getElementById('threejs-canvas');
        canvas.addEventListener('dragover', (e) => {
            e.preventDefault();
        });

        canvas.addEventListener('drop', (e) => {
            e.preventDefault();
            const gateType = e.dataTransfer.getData('text/plain');
            if (gateType) {
                this.handleGateDrop(gateType, e);
            }
        });
    }

    // Circuit Management
    newCircuit() {
        const qubitCount = prompt('Enter number of qubits:', '2');
        if (qubitCount && !isNaN(qubitCount)) {
            this.currentCircuit = this.quantumCircuit.createCircuit(parseInt(qubitCount));
            this.quantumVisualizer.updateCircuit(this.currentCircuit);
            this.updateCircuitInfo();
            this.logToConsole(`Created new circuit with ${qubitCount} qubits`);
        }
    }

    loadCircuit() {
        // TODO: Implement circuit loading
        this.logToConsole('Circuit loading not yet implemented');
    }

    saveCircuit() {
        // TODO: Implement circuit saving
        this.logToConsole('Circuit saving not yet implemented');
    }

    playCircuit() {
        if (this.currentCircuit) {
            this.quantumVisualizer.playAnimation();
            this.logToConsole('Playing circuit animation');
        }
    }

    pauseCircuit() {
        this.quantumVisualizer.pauseAnimation();
        this.logToConsole('Paused circuit animation');
    }

    resetCircuit() {
        this.quantumVisualizer.resetAnimation();
        this.updateQuantumState();
        this.logToConsole('Reset circuit to initial state');
    }

    addQubit() {
        if (this.currentCircuit) {
            this.quantumCircuit.addQubit(this.currentCircuit);
            this.quantumVisualizer.updateCircuit(this.currentCircuit);
            this.updateCircuitInfo();
            this.logToConsole('Added new qubit');
        }
    }

    removeQubit() {
        if (this.currentCircuit && this.currentCircuit.numQubits > 1) {
            this.quantumCircuit.removeQubit(this.currentCircuit);
            this.quantumVisualizer.updateCircuit(this.currentCircuit);
            this.updateCircuitInfo();
            this.logToConsole('Removed qubit');
        }
    }

    // 3D Scene Controls
    resetCamera() {
        this.quantumVisualizer.resetCamera();
    }

    toggleGrid() {
        this.quantumVisualizer.toggleGrid();
    }

    toggleAxes() {
        this.quantumVisualizer.toggleAxes();
    }

    // Gate Handling
    handleGateDrop(gateType, event) {
        // TODO: Implement gate placement based on drop position
        this.logToConsole(`Dropped gate: ${gateType}`);
    }

    // IBM Integration
    showIBMModal() {
        document.getElementById('ibm-modal').classList.remove('hidden');
    }

    hideIBMModal() {
        document.getElementById('ibm-modal').classList.add('hidden');
    }

    async connectIBM() {
        const token = document.getElementById('ibm-token').value;
        if (!token) {
            this.showError('Please enter IBM Quantum token');
            return;
        }

        try {
            await this.ibmIntegration.connect(token);
            this.logToConsole('Connected to IBM Quantum');
            this.hideIBMModal();
            this.showIBMDevices();
        } catch (error) {
            this.showError('Failed to connect to IBM Quantum: ' + error.message);
        }
    }

    async showIBMDevices() {
        try {
            const devices = await this.ibmIntegration.getDevices();
            const deviceList = document.getElementById('device-list');
            deviceList.innerHTML = '';

            devices.forEach(device => {
                const deviceElement = document.createElement('div');
                deviceElement.className = 'device-item';
                deviceElement.innerHTML = `
                    <div class="device-name">${device.name}</div>
                    <div class="device-status ${device.status}">Status: ${device.status}</div>
                    <div class="device-queue">Queue: ${device.queue}</div>
                `;
                deviceList.appendChild(deviceElement);
            });

            document.getElementById('ibm-devices').style.display = 'block';
        } catch (error) {
            this.showError('Failed to load devices: ' + error.message);
        }
    }

    // UI Updates
    updateCircuitInfo() {
        if (this.currentCircuit) {
            document.getElementById('qubit-count').textContent = this.currentCircuit.numQubits;
            document.getElementById('circuit-depth').textContent = this.quantumCircuit.getDepth(this.currentCircuit);
            document.getElementById('gate-count').textContent = this.quantumCircuit.getGateCount(this.currentCircuit);
        }
    }

    updateQuantumState() {
        const stateDisplay = document.getElementById('quantum-state-display');
        // TODO: Implement quantum state visualization
    }

    // Console Management
    logToConsole(message) {
        const consoleOutput = document.getElementById('console-output');
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.className = 'console-entry';
        logEntry.innerHTML = `<span class="timestamp">[${timestamp}]</span> ${message}`;
        consoleOutput.appendChild(logEntry);
        consoleOutput.scrollTop = consoleOutput.scrollHeight;
    }

    clearConsole() {
        document.getElementById('console-output').innerHTML = '';
    }

    // Sidebar Management
    toggleSidebar(side) {
        const sidebar = side === 'left' ? document.querySelector('.left-sidebar') :
                      document.querySelector('.right-sidebar');
        const collapseBtn = side === 'left' ? document.getElementById('gate-collapse') :
                          document.getElementById('properties-collapse');

        sidebar.classList.toggle('collapsed');

        const icon = collapseBtn.querySelector('i');
        if (sidebar.classList.contains('collapsed')) {
            icon.className = side === 'left' ? 'fas fa-chevron-right' : 'fas fa-chevron-left';
        } else {
            icon.className = side === 'left' ? 'fas fa-chevron-left' : 'fas fa-chevron-right';
        }
    }

    // Error Handling
    showError(message) {
        this.logToConsole(`ERROR: ${message}`);

        // Hide loading screen
        this.hideLoadingScreen();

        // Show error message in the canvas area
        const canvasContainer = document.querySelector('.canvas-container');
        if (canvasContainer) {
            canvasContainer.innerHTML = `
                <div style="
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100%;
                    color: #ff6b6b;
                    font-family: 'Inter', sans-serif;
                    text-align: center;
                    padding: 20px;
                    background: rgba(0, 0, 0, 0.8);
                    border-radius: 10px;
                    margin: 20px;
                ">
                    <i class="fas fa-exclamation-triangle" style="font-size: 3em; margin-bottom: 20px;"></i>
                    <h2>Initialization Failed</h2>
                    <p style="margin-bottom: 20px;">${message}</p>
                    <div style="display: flex; gap: 10px;">
                        <button onclick="location.reload()" style="
                            background: #00ffff;
                            color: #000;
                            border: none;
                            padding: 10px 20px;
                            border-radius: 5px;
                            cursor: pointer;
                        ">Retry</button>
                        <a href="debug.html" style="
                            background: #666;
                            color: #fff;
                            text-decoration: none;
                            padding: 10px 20px;
                            border-radius: 5px;
                            display: inline-block;
                        ">Debug</a>
                    </div>
                </div>
            `;
        }

        // Also show alert as fallback
        alert(`Application Error: ${message}\n\nCheck the browser console for details.`);
    }
}

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.quantumApp = new QuantumVisualizerApp();
});

// Global error handling
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    if (window.quantumApp) {
        window.quantumApp.logToConsole(`Runtime Error: ${event.error.message}`);
    }
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    if (window.quantumApp) {
        window.quantumApp.logToConsole(`Promise Rejection: ${event.reason}`);
    }
});
