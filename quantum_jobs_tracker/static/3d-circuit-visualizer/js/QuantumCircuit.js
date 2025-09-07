// Quantum Circuit Logic - Qiskit Integration and Circuit Management
// Handles quantum circuit creation, gate operations, and state simulation

class QuantumCircuit {
    constructor() {
        this.circuit = null;
        this.stateVector = null;
        this.measurementResults = null;
        this.gateHistory = [];

        this.init();
    }

    init() {
        // Initialize with basic circuit
        this.createCircuit(2);
    }

    createCircuit(numQubits, numClassicalBits = null) {
        try {
            // Using our custom quantum simulator
            this.circuit = window.quantumSimulator.createCircuit(numQubits, numClassicalBits || numQubits);

            // Initialize state vector
            this.stateVector = this.initializeStateVector(numQubits);

            // Reset gate history
            this.gateHistory = [];

            console.log(`Created quantum circuit with ${numQubits} qubits`);
            return this.circuit;
        } catch (error) {
            console.error('Failed to create quantum circuit:', error);
            throw error;
        }
    }

    initializeStateVector(numQubits) {
        const size = Math.pow(2, numQubits);
        const stateVector = new Array(size).fill(0);
        stateVector[0] = 1; // Initialize to |00...0⟩ state
        return stateVector;
    }

    // Gate Operations
    addGate(gateType, qubitIndex, controlIndex = null, angle = null) {
        if (!this.circuit) {
            throw new Error('No quantum circuit initialized');
        }

        try {
            // Use quantum simulator to apply gate
            window.quantumSimulator.applyGate(gateType, qubitIndex, controlIndex, angle);

            // Record gate in history
            this.gateHistory.push({
                type: gateType,
                qubit: qubitIndex,
                control: controlIndex,
                angle: angle,
                timestamp: Date.now()
            });

            // Update our state vector from simulator
            this.stateVector = window.quantumSimulator.getStateVector();

            console.log(`Added ${gateType} gate to qubit ${qubitIndex}`);
        } catch (error) {
            console.error(`Failed to add ${gateType} gate:`, error);
            throw error;
        }
    }

    // Circuit Management
    addQubit() {
        if (!this.circuit) return;

        const newNumQubits = this.circuit.numQubits + 1;
        const newCircuit = this.createCircuit(newNumQubits);
        this.copyGatesToNewCircuit(newCircuit);

        return newCircuit;
    }

    removeQubit() {
        if (!this.circuit || this.circuit.numQubits <= 1) return;

        const newNumQubits = this.circuit.numQubits - 1;
        const newCircuit = this.createCircuit(newNumQubits);
        // Only copy gates that don't reference the removed qubit
        this.copyValidGatesToNewCircuit(newCircuit);

        return newCircuit;
    }

    copyGatesToNewCircuit(newCircuit) {
        this.gateHistory.forEach(gate => {
            try {
                newCircuit.addGate(gate.type, gate.qubit, gate.control, gate.angle);
            } catch (error) {
                console.warn(`Could not copy gate ${gate.type}:`, error);
            }
        });
    }

    copyValidGatesToNewCircuit(newCircuit) {
        this.gateHistory.forEach(gate => {
            if (gate.qubit < newCircuit.numQubits &&
                (gate.control === null || gate.control < newCircuit.numQubits)) {
                try {
                    newCircuit.addGate(gate.type, gate.qubit, gate.control, gate.angle);
                } catch (error) {
                    console.warn(`Could not copy gate ${gate.type}:`, error);
                }
            }
        });
    }

    // Circuit Analysis
    getDepth() {
        if (!this.circuit) return 0;
        // TODO: Implement circuit depth calculation
        return this.gateHistory.length;
    }

    getGateCount() {
        return this.gateHistory.length;
    }

    getCircuitMatrix() {
        if (!this.circuit) return null;
        // TODO: Implement circuit matrix calculation
        return null;
    }

    // State Vector Simulation
    updateStateVector() {
        // TODO: Implement state vector evolution
        // This would typically involve matrix multiplication
        // For now, we'll use a simplified approach
    }

    getStateVector() {
        return this.stateVector;
    }

    getProbabilityDistribution() {
        if (!this.stateVector) return null;

        const probabilities = this.stateVector.map(amplitude =>
            Math.pow(amplitude, 2)
        );

        return probabilities;
    }

    // Measurement Operations
    measure(qubitIndex, shots = 1024) {
        if (!this.circuit) {
            throw new Error('No quantum circuit initialized');
        }

        try {
            // Add measurement to circuit
            this.circuit.measure(qubitIndex, qubitIndex);

            // Simulate measurement results
            this.measurementResults = this.simulateMeasurements(shots);

            return this.measurementResults;
        } catch (error) {
            console.error('Measurement failed:', error);
            throw error;
        }
    }

    simulateMeasurements(shots) {
        // Simplified measurement simulation
        const probabilities = this.getProbabilityDistribution();
        const results = {};

        for (let i = 0; i < shots; i++) {
            const random = Math.random();
            let cumulativeProb = 0;
            let outcome = 0;

            for (let j = 0; j < probabilities.length; j++) {
                cumulativeProb += probabilities[j];
                if (random <= cumulativeProb) {
                    outcome = j;
                    break;
                }
            }

            const binaryString = outcome.toString(2).padStart(this.circuit.numQubits, '0');
            results[binaryString] = (results[binaryString] || 0) + 1;
        }

        return results;
    }

    getMeasurementResults() {
        return this.measurementResults;
    }

    // Circuit Export/Import
    exportCircuit() {
        if (!this.circuit) return null;

        return {
            numQubits: this.circuit.numQubits,
            numClassicalBits: this.circuit.numClassicalBits,
            gates: this.gateHistory,
            stateVector: this.stateVector,
            measurementResults: this.measurementResults
        };
    }

    importCircuit(circuitData) {
        try {
            this.createCircuit(circuitData.numQubits, circuitData.numClassicalBits);
            this.gateHistory = circuitData.gates || [];
            this.stateVector = circuitData.stateVector || this.initializeStateVector(circuitData.numQubits);
            this.measurementResults = circuitData.measurementResults;

            // Rebuild circuit from gate history
            this.gateHistory.forEach(gate => {
                this.addGate(gate.type, gate.qubit, gate.control, gate.angle);
            });

            console.log('Circuit imported successfully');
        } catch (error) {
            console.error('Failed to import circuit:', error);
            throw error;
        }
    }

    // Utility Methods
    reset() {
        this.circuit = null;
        this.stateVector = null;
        this.measurementResults = null;
        this.gateHistory = [];
    }

    getCircuitInfo() {
        if (!this.circuit) return null;

        return {
            numQubits: this.circuit.numQubits,
            numClassicalBits: this.circuit.numClassicalBits,
            depth: this.getDepth(),
            gateCount: this.getGateCount(),
            gates: this.gateHistory
        };
    }

    // Advanced Quantum Operations
    applyEntanglingGate(qubit1, qubit2, gateType = 'CNOT') {
        this.addGate(gateType, qubit1, qubit2);
    }

    createBellState(qubit1, qubit2) {
        // Create |00⟩ + |11⟩ Bell state
        this.addGate('H', qubit1);
        this.addGate('CNOT', qubit1, qubit2);
    }

    createGHZState(qubits) {
        // Create GHZ state |00...0⟩ + |11...1⟩
        this.addGate('H', qubits[0]);
        for (let i = 1; i < qubits.length; i++) {
            this.addGate('CNOT', qubits[i-1], qubits[i]);
        }
    }

    // Quantum Fourier Transform
    applyQFT(qubits) {
        for (let i = 0; i < qubits.length; i++) {
            this.addGate('H', qubits[i]);
            for (let j = i + 1; j < qubits.length; j++) {
                const angle = Math.PI / Math.pow(2, j - i);
                this.addGate('CRZ', qubits[j], qubits[i], angle);
            }
        }
    }

    // Inverse QFT
    applyIQFT(qubits) {
        for (let i = qubits.length - 1; i >= 0; i--) {
            for (let j = qubits.length - 1; j > i; j--) {
                const angle = -Math.PI / Math.pow(2, j - i);
                this.addGate('CRZ', qubits[j], qubits[i], angle);
            }
            this.addGate('H', qubits[i]);
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QuantumCircuit;
}
