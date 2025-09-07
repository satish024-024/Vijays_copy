// 3D Quantum Circuit Visualizer - Three.js Implementation
// Handles 3D rendering, camera controls, and quantum state visualization

class QuantumVisualizer {
    constructor(canvasId) {
        this.canvasId = canvasId;
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.animationId = null;
        this.isAnimating = false;

        // Scene objects
        this.qubits = [];
        this.gates = [];
        this.grid = null;
        this.axes = null;

        // Quantum state visualization
        this.blochSpheres = [];
        this.stateVectors = [];

        this.init();
    }

    init() {
        try {
            console.log('Setting up Three.js scene...');
            this.setupScene();

            console.log('Setting up camera...');
            this.setupCamera();

            console.log('Setting up renderer...');
            this.setupRenderer();

            console.log('Setting up controls...');
            this.setupControls();

            console.log('Setting up lighting...');
            this.setupLighting();

            console.log('Creating grid...');
            this.createGrid();

            console.log('Creating axes...');
            this.createAxes();

            console.log('Setting up event listeners...');
            this.setupEventListeners();

            console.log('Starting animation loop...');
            this.animate();

            console.log('QuantumVisualizer initialized successfully');
        } catch (error) {
            console.error('Failed to initialize QuantumVisualizer:', error);
            throw error;
        }
    }

    setupScene() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0a0a0a);
        this.scene.fog = new THREE.Fog(0x0a0a0a, 50, 200);
    }

    setupCamera() {
        const canvas = document.getElementById(this.canvasId);
        const aspect = canvas.clientWidth / canvas.clientHeight;

        this.camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);
        this.camera.position.set(20, 15, 20);
        this.camera.lookAt(0, 0, 0);
    }

    setupRenderer() {
        const canvas = document.getElementById(this.canvasId);

        if (!canvas) {
            throw new Error(`Canvas element with ID '${this.canvasId}' not found`);
        }

        console.log('Canvas element found:', canvas);

        // Ensure canvas has proper dimensions
        if (canvas.clientWidth === 0 || canvas.clientHeight === 0) {
            console.warn('Canvas has zero dimensions, setting default size');
            canvas.style.width = '800px';
            canvas.style.height = '600px';
        }

        try {
            // Check if WebGL is supported
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            if (!gl) {
                throw new Error('WebGL not supported');
            }

            this.renderer = new THREE.WebGLRenderer({
                canvas: canvas,
                antialias: true,
                alpha: true
            });

            // Test renderer by clearing it
            this.renderer.clear();

        } catch (error) {
            console.error('Failed to create WebGL renderer:', error);

            // Create a fallback message
            canvas.innerHTML = `
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
                ">
                    <i class="fas fa-exclamation-triangle" style="font-size: 3em; margin-bottom: 20px;"></i>
                    <h3>3D Visualization Not Available</h3>
                    <p>${error.message}</p>
                    <p style="font-size: 0.9em; margin-top: 10px;">
                        Please ensure your browser supports WebGL and try refreshing the page.
                    </p>
                </div>
            `;

            throw error;
        }

        this.renderer.setSize(canvas.clientWidth, canvas.clientHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Limit pixel ratio for performance
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        // --------------------------------------------------
        if (!('outputColorSpace' in this.renderer)) {
            Object.defineProperty(this.renderer, 'outputColorSpace', {
                configurable:true,
                enumerable:true,
                get(){ return this.outputEncoding; },
                set(v){ this.outputEncoding = v; }
            });
        }
        if (typeof THREE.SRGBColorSpace === 'undefined') {
            THREE.SRGBColorSpace = THREE.sRGBEncoding || 3000;
        }
        this.renderer.outputColorSpace = THREE.SRGBColorSpace;
        // --------------------------------------------------

        console.log('Renderer created successfully');
    }

    setupControls() {
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.screenSpacePanning = false;
        this.controls.minDistance = 5;
        this.controls.maxDistance = 100;
        this.controls.maxPolarAngle = Math.PI;
    }

    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.3);
        this.scene.add(ambientLight);

        // Main directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        this.scene.add(directionalLight);

        // Secondary light for quantum effects
        const quantumLight = new THREE.PointLight(0x00ffff, 0.5, 50);
        quantumLight.position.set(-10, 10, -10);
        this.scene.add(quantumLight);

        // Rim lighting
        const rimLight = new THREE.DirectionalLight(0x0088ff, 0.3);
        rimLight.position.set(-5, 5, -5);
        this.scene.add(rimLight);
    }

    createGrid() {
        const gridHelper = new THREE.GridHelper(50, 50, 0x444444, 0x222222);
        gridHelper.position.y = -5;
        this.grid = gridHelper;
        this.scene.add(gridHelper);
    }

    createAxes() {
        const axesHelper = new THREE.AxesHelper(10);
        this.axes = axesHelper;
        this.scene.add(axesHelper);
    }

    setupEventListeners() {
        window.addEventListener('resize', () => this.onWindowResize());

        // Canvas click events for gate selection
        const canvas = document.getElementById(this.canvasId);
        if (canvas) {
            canvas.addEventListener('click', (event) => this.onCanvasClick(event));
        } else {
            console.warn(`Canvas element with ID '${this.canvasId}' not found for event listeners`);
        }
    }

    onWindowResize() {
        const canvas = document.getElementById(this.canvasId);
        if (canvas && this.camera && this.renderer) {
            this.camera.aspect = canvas.clientWidth / canvas.clientHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(canvas.clientWidth, canvas.clientHeight);
        }
    }

    onCanvasClick(event) {
        const canvas = document.getElementById(this.canvasId);
        if (!canvas) return;
        const rect = canvas.getBoundingClientRect();

        const mouse = new THREE.Vector2();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(mouse, this.camera);

        const intersects = raycaster.intersectObjects(this.scene.children, true);

        if (intersects.length > 0) {
            const clickedObject = intersects[0].object;
            this.handleObjectClick(clickedObject);
        }
    }

    handleObjectClick(object) {
        // Handle clicks on quantum objects
        if (object.userData && object.userData.type === 'qubit') {
            this.selectQubit(object.userData.qubitIndex);
        } else if (object.userData && object.userData.type === 'gate') {
            this.selectGate(object.userData.gateId);
        }
    }

    // Circuit Visualization
    updateCircuit(circuit) {
        this.clearCircuit();
        this.createQubits(circuit.numQubits);
        this.createGates(circuit);
    }

    createQubits(numQubits) {
        this.qubits = [];

        for (let i = 0; i < numQubits; i++) {
            const qubit = this.createQubit(i, numQubits);
            this.qubits.push(qubit);
            this.scene.add(qubit);
        }
    }

    createQubit(index, totalQubits) {
        const geometry = new THREE.SphereGeometry(0.3, 32, 32);
        const material = new THREE.MeshPhongMaterial({
            color: 0x00ffff,
            emissive: 0x002222,
            transparent: true,
            opacity: 0.8
        });

        const qubit = new THREE.Mesh(geometry, material);
        qubit.position.set(0, index * 2 - (totalQubits - 1), 0);
        qubit.userData = { type: 'qubit', qubitIndex: index };

        // Add glow effect
        const glowGeometry = new THREE.SphereGeometry(0.35, 32, 32);
        const glowMaterial = new THREE.MeshBasicMaterial({
            color: 0x00ffff,
            transparent: true,
            opacity: 0.2
        });
        const glow = new THREE.Mesh(glowGeometry, glowMaterial);
        qubit.add(glow);

        return qubit;
    }

    createGates(circuit) {
        // TODO: Implement gate creation based on circuit data
        // This will be called when gates are added to the circuit
    }

    createGate(gateType, position, qubitIndex) {
        const gate3D = new Gate3D(gateType, position, qubitIndex);
        this.gates.push(gate3D);
        this.scene.add(gate3D.mesh);
        return gate3D;
    }

    clearCircuit() {
        // Remove existing qubits and gates
        this.qubits.forEach(qubit => {
            this.scene.remove(qubit);
        });
        this.gates.forEach(gate => {
            this.scene.remove(gate.mesh);
        });

        this.qubits = [];
        this.gates = [];
    }

    // Animation and Controls
    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());

        try {
            if (this.controls) {
                this.controls.update();
            }

            // Update quantum animations
            this.updateQuantumAnimations();

            // Render the scene
            if (this.renderer && this.scene && this.camera) {
                this.renderer.render(this.scene, this.camera);
            } else {
                console.warn('Missing renderer, scene, or camera for animation');
            }
        } catch (error) {
            console.error('Animation error:', error);
            // Stop animation on error to prevent console spam
            if (this.animationId) {
                cancelAnimationFrame(this.animationId);
                this.animationId = null;
            }
        }
    }

    updateQuantumAnimations() {
        const time = Date.now() * 0.001;

        // Animate qubits
        this.qubits.forEach((qubit, index) => {
            qubit.rotation.y = time * 0.5;
            qubit.position.y += Math.sin(time + index) * 0.002;
        });

        // Animate gates
        this.gates.forEach(gate => {
            if (gate.mesh) {
                gate.updateAnimation(time);
            }
        });
    }

    playAnimation() {
        this.isAnimating = true;
        // TODO: Implement circuit execution animation
    }

    pauseAnimation() {
        this.isAnimating = false;
    }

    resetAnimation() {
        this.isAnimating = false;
        // Reset all objects to initial positions
        this.qubits.forEach(qubit => {
            qubit.position.y = qubit.userData.originalY || qubit.position.y;
            qubit.rotation.set(0, 0, 0);
        });
    }

    // Camera Controls
    resetCamera() {
        this.camera.position.set(20, 15, 20);
        this.camera.lookAt(0, 0, 0);
        this.controls.reset();
    }

    toggleGrid() {
        if (this.grid) {
            this.grid.visible = !this.grid.visible;
        }
    }

    toggleAxes() {
        if (this.axes) {
            this.axes.visible = !this.axes.visible;
        }
    }

    // Selection Methods
    selectQubit(index) {
        // Highlight selected qubit
        this.qubits.forEach((qubit, i) => {
            if (i === index) {
                qubit.material.emissive.setHex(0x004444);
            } else {
                qubit.material.emissive.setHex(0x002222);
            }
        });
    }

    selectGate(gateId) {
        // TODO: Implement gate selection
    }

    // Quantum State Visualization
    updateQuantumState(stateVector) {
        // Update Bloch spheres and state vectors
        this.updateBlochSpheres(stateVector);
        this.updateStateVectors(stateVector);
    }

    updateBlochSpheres(stateVector) {
        // TODO: Implement Bloch sphere updates
    }

    updateStateVectors(stateVector) {
        // TODO: Implement state vector visualization
    }

    // Utility Methods
    getWorldPositionFromScreen(screenX, screenY) {
        const canvas = document.getElementById(this.canvasId);
        const rect = canvas.getBoundingClientRect();

        const mouse = new THREE.Vector2();
        mouse.x = ((screenX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((screenY - rect.top) / rect.height) * 2 + 1;

        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(mouse, this.camera);

        // Find intersection with quantum plane (XZ plane at y=0)
        const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
        const intersection = new THREE.Vector3();
        raycaster.ray.intersectPlane(plane, intersection);

        return intersection;
    }

    dispose() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }

        if (this.renderer) {
            this.renderer.dispose();
        }

        // Dispose of geometries and materials
        this.scene.traverse((object) => {
            if (object.geometry) {
                object.geometry.dispose();
            }
            if (object.material) {
                if (Array.isArray(object.material)) {
                    object.material.forEach(material => material.dispose());
                } else {
                    object.material.dispose();
                }
            }
        });
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QuantumVisualizer;
}
