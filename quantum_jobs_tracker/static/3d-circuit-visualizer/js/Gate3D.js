// 3D Gate Visualization - Three.js Gate Objects
// Creates and manages 3D representations of quantum gates

class Gate3D {
    constructor(gateType, position, qubitIndex) {
        this.gateType = gateType;
        this.position = position || new THREE.Vector3(0, 0, 0);
        this.qubitIndex = qubitIndex;
        this.mesh = null;
        this.glowMesh = null;
        this.animationPhase = 0;

        this.createGateMesh();
    }

    createGateMesh() {
        const gateConfig = this.getGateConfig();
        const geometry = this.createGateGeometry(gateConfig);
        const material = this.createGateMaterial(gateConfig);

        this.mesh = new THREE.Mesh(geometry, material);
        this.mesh.position.copy(this.position);
        this.mesh.userData = {
            type: 'gate',
            gateType: this.gateType,
            qubitIndex: this.qubitIndex,
            gateId: `${this.gateType}_${this.qubitIndex}_${Date.now()}`
        };

        // Add glow effect
        this.createGlowEffect(gateConfig);

        // Add wire connections for multi-qubit gates
        if (gateConfig.multiQubit) {
            this.createWireConnections(gateConfig);
        }
    }

    getGateConfig() {
        const configs = {
            'H': {
                color: 0xffaa00,
                emissive: 0x442200,
                shape: 'cube',
                size: 0.8,
                multiQubit: false
            },
            'X': {
                color: 0xff4444,
                emissive: 0x220000,
                shape: 'sphere',
                size: 0.6,
                multiQubit: false
            },
            'Y': {
                color: 0x44ff44,
                emissive: 0x002200,
                shape: 'cylinder',
                size: 0.6,
                multiQubit: false
            },
            'Z': {
                color: 0x4444ff,
                emissive: 0x000022,
                shape: 'ring',
                size: 0.7,
                multiQubit: false
            },
            'S': {
                color: 0xff44ff,
                emissive: 0x220022,
                shape: 'octahedron',
                size: 0.5,
                multiQubit: false
            },
            'T': {
                color: 0x44ffff,
                emissive: 0x002222,
                shape: 'tetrahedron',
                size: 0.5,
                multiQubit: false
            },
            'CNOT': {
                color: 0xff8800,
                emissive: 0x331100,
                shape: 'torus',
                size: 0.8,
                multiQubit: true
            },
            'CZ': {
                color: 0x8800ff,
                emissive: 0x110033,
                shape: 'doubleRing',
                size: 0.8,
                multiQubit: true
            },
            'SWAP': {
                color: 0x00ff88,
                emissive: 0x003311,
                shape: 'cross',
                size: 0.7,
                multiQubit: true
            },
            'MEASURE': {
                color: 0xffffff,
                emissive: 0x222222,
                shape: 'meter',
                size: 0.6,
                multiQubit: false
            }
        };

        return configs[this.gateType] || configs['H'];
    }

    createGateGeometry(config) {
        let geometry;

        switch (config.shape) {
            case 'cube':
                geometry = new THREE.BoxGeometry(config.size, config.size, config.size);
                break;
            case 'sphere':
                geometry = new THREE.SphereGeometry(config.size, 16, 16);
                break;
            case 'cylinder':
                geometry = new THREE.CylinderGeometry(config.size * 0.5, config.size * 0.5, config.size, 16);
                break;
            case 'ring':
                geometry = new THREE.RingGeometry(config.size * 0.3, config.size * 0.7, 16);
                break;
            case 'octahedron':
                geometry = new THREE.OctahedronGeometry(config.size);
                break;
            case 'tetrahedron':
                geometry = new THREE.TetrahedronGeometry(config.size);
                break;
            case 'torus':
                geometry = new THREE.TorusGeometry(config.size * 0.5, config.size * 0.2, 8, 16);
                break;
            case 'doubleRing':
                geometry = this.createDoubleRingGeometry(config.size);
                break;
            case 'cross':
                geometry = this.createCrossGeometry(config.size);
                break;
            case 'meter':
                geometry = this.createMeterGeometry(config.size);
                break;
            default:
                geometry = new THREE.BoxGeometry(config.size, config.size, config.size);
        }

        return geometry;
    }

    createDoubleRingGeometry(size) {
        const geometry = new THREE.RingGeometry(size * 0.2, size * 0.4, 16);
        const secondRing = new THREE.RingGeometry(size * 0.5, size * 0.7, 16);

        // Combine geometries (simplified approach)
        return geometry;
    }

    createCrossGeometry(size) {
        const geometry = new THREE.BoxGeometry(size * 0.2, size, size * 0.2);
        return geometry;
    }

    createMeterGeometry(size) {
        const geometry = new THREE.CylinderGeometry(size * 0.3, size * 0.3, size * 0.1, 8);
        return geometry;
    }

    createGateMaterial(config) {
        return new THREE.MeshPhongMaterial({
            color: config.color,
            emissive: config.emissive,
            transparent: true,
            opacity: 0.9,
            shininess: 100
        });
    }

    createGlowEffect(config) {
        const glowGeometry = this.createGateGeometry(config);
        const glowMaterial = new THREE.MeshBasicMaterial({
            color: config.color,
            transparent: true,
            opacity: 0.3
        });

        this.glowMesh = new THREE.Mesh(glowGeometry, glowMaterial);
        this.glowMesh.scale.setScalar(1.2);
        this.mesh.add(this.glowMesh);
    }

    createWireConnections(config) {
        // Create connecting lines between qubits for multi-qubit gates
        const wireMaterial = new THREE.LineBasicMaterial({
            color: config.color,
            transparent: true,
            opacity: 0.6
        });

        const wireGeometry = new THREE.BufferGeometry();
        const points = [
            new THREE.Vector3(0, 0, 0),
            new THREE.Vector3(0, 2, 0) // Connect to qubit above
        ];

        wireGeometry.setFromPoints(points);
        const wire = new THREE.Line(wireGeometry, wireMaterial);
        this.mesh.add(wire);

        // Add control dot for control qubits
        const controlGeometry = new THREE.SphereGeometry(0.1, 8, 8);
        const controlMaterial = new THREE.MeshBasicMaterial({
            color: 0x000000
        });
        const controlDot = new THREE.Mesh(controlGeometry, controlMaterial);
        controlDot.position.set(0, 1, 0);
        this.mesh.add(controlDot);
    }

    updateAnimation(time) {
        if (!this.mesh) return;

        // Rotate the gate
        this.mesh.rotation.y = time * 0.5;
        this.mesh.rotation.x = Math.sin(time) * 0.1;

        // Pulse the glow effect
        if (this.glowMesh) {
            const scale = 1.2 + Math.sin(time * 2) * 0.1;
            this.glowMesh.scale.setScalar(scale);
            this.glowMesh.material.opacity = 0.3 + Math.sin(time * 2) * 0.1;
        }

        // Special animations for specific gates
        this.applySpecialAnimations(time);
    }

    applySpecialAnimations(time) {
        switch (this.gateType) {
            case 'H':
                // Hadamard gate: superposition visualization
                this.mesh.position.y = this.position.y + Math.sin(time * 3) * 0.1;
                break;
            case 'X':
                // Pauli-X: flip animation
                this.mesh.rotation.z = Math.sin(time * 2) * Math.PI;
                break;
            case 'Y':
                // Pauli-Y: phase rotation
                this.mesh.rotation.z = time;
                break;
            case 'Z':
                // Pauli-Z: phase shift visualization
                if (this.glowMesh) {
                    this.glowMesh.material.color.setHSL((time * 0.1) % 1, 1, 0.5);
                }
                break;
            case 'MEASURE':
                // Measurement: collapse animation
                const collapse = Math.sin(time * 5) * 0.05;
                this.mesh.scale.setScalar(1 + collapse);
                break;
        }
    }

    setPosition(position) {
        this.position.copy(position);
        if (this.mesh) {
            this.mesh.position.copy(position);
        }
    }

    setHighlight(highlighted) {
        if (this.mesh && this.mesh.material) {
            if (highlighted) {
                this.mesh.material.emissive.setHex(0x444444);
                if (this.glowMesh) {
                    this.glowMesh.material.opacity = 0.6;
                }
            } else {
                const config = this.getGateConfig();
                this.mesh.material.emissive.setHex(config.emissive);
                if (this.glowMesh) {
                    this.glowMesh.material.opacity = 0.3;
                }
            }
        }
    }

    dispose() {
        if (this.mesh) {
            if (this.mesh.geometry) {
                this.mesh.geometry.dispose();
            }
            if (this.mesh.material) {
                this.mesh.material.dispose();
            }
        }

        if (this.glowMesh) {
            if (this.glowMesh.geometry) {
                this.glowMesh.geometry.dispose();
            }
            if (this.glowMesh.material) {
                this.glowMesh.material.dispose();
            }
        }
    }

    // Utility methods
    getBoundingBox() {
        if (!this.mesh) return null;

        const box = new THREE.Box3().setFromObject(this.mesh);
        return box;
    }

    intersectsRay(raycaster) {
        if (!this.mesh) return false;

        const intersects = raycaster.intersectObject(this.mesh, true);
        return intersects.length > 0;
    }

    clone() {
        const cloned = new Gate3D(this.gateType, this.position.clone(), this.qubitIndex);
        return cloned;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Gate3D;
}
