// Quantum Simulator - Basic quantum computing functionality
// Simplified quantum simulator for browser-based quantum circuit simulation

class QuantumSimulator {
    constructor() {
        this.circuits = new Map();
        this.currentCircuit = null;
        this.results = new Map();
    }

    // Create a new quantum circuit
    createCircuit(numQubits, numClassicalBits = null) {
        const circuitId = `circuit_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        const circuit = {
            id: circuitId,
            numQubits: numQubits,
            numClassicalBits: numClassicalBits || numQubits,
            gates: [],
            measurements: [],
            stateVector: this.initializeStateVector(numQubits)
        };

        this.circuits.set(circuitId, circuit);
        this.currentCircuit = circuit;
        return circuit;
    }

    // Initialize quantum state vector
    initializeStateVector(numQubits) {
        const size = Math.pow(2, numQubits);
        const stateVector = new Array(size).fill(0);
        stateVector[0] = 1; // |00...0⟩ state
        return stateVector;
    }

    // Get current circuit
    getCurrentCircuit() {
        return this.currentCircuit;
    }

    // Apply quantum gate to circuit
    applyGate(gateType, qubitIndex, controlIndex = null, angle = 0) {
        if (!this.currentCircuit) {
            throw new Error('No active circuit');
        }

        const gate = {
            type: gateType,
            qubit: qubitIndex,
            control: controlIndex,
            angle: angle,
            timestamp: Date.now()
        };

        this.currentCircuit.gates.push(gate);
        this.updateStateVector(gate);
    }

    // Update quantum state vector after applying a gate
    updateStateVector(gate) {
        // Simplified state vector evolution
        // In a real implementation, this would apply unitary matrices
        const circuit = this.currentCircuit;
        const numQubits = circuit.numQubits;

        switch (gate.type.toUpperCase()) {
            case 'H': // Hadamard gate
                this.applyHadamard(circuit.stateVector, gate.qubit, numQubits);
                break;
            case 'X': // Pauli-X gate
                this.applyPauliX(circuit.stateVector, gate.qubit, numQubits);
                break;
            case 'Y': // Pauli-Y gate
                this.applyPauliY(circuit.stateVector, gate.qubit, numQubits);
                break;
            case 'Z': // Pauli-Z gate
                this.applyPauliZ(circuit.stateVector, gate.qubit, numQubits);
                break;
            case 'CNOT': // CNOT gate
                this.applyCNOT(circuit.stateVector, gate.control, gate.qubit, numQubits);
                break;
            case 'MEASURE': // Measurement
                this.applyMeasurement(gate.qubit, circuit);
                break;
        }
    }

    // Hadamard gate implementation
    applyHadamard(stateVector, qubit, numQubits) {
        const newState = new Array(stateVector.length).fill(0);
        const sqrt2 = Math.sqrt(0.5);

        for (let i = 0; i < stateVector.length; i++) {
            const bit = (i >> qubit) & 1;
            const flippedBit = i ^ (1 << qubit);

            if (bit === 0) {
                newState[i] += sqrt2 * stateVector[i];
                newState[flippedBit] += sqrt2 * stateVector[i];
            } else {
                newState[i] += sqrt2 * stateVector[i];
                newState[flippedBit] -= sqrt2 * stateVector[i];
            }
        }

        // Copy back to original array
        for (let i = 0; i < stateVector.length; i++) {
            stateVector[i] = newState[i];
        }
    }

    // Pauli-X gate implementation
    applyPauliX(stateVector, qubit, numQubits) {
        const newState = new Array(stateVector.length).fill(0);

        for (let i = 0; i < stateVector.length; i++) {
            const flippedBit = i ^ (1 << qubit);
            newState[flippedBit] = stateVector[i];
        }

        // Copy back to original array
        for (let i = 0; i < stateVector.length; i++) {
            stateVector[i] = newState[i];
        }
    }

    // Pauli-Y gate implementation
    applyPauliY(stateVector, qubit, numQubits) {
        // For now, implement as a simple phase gate (simplified)
        // Pauli-Y = [[0, -i], [i, 0]]
        // We'll implement this as a phase shift for simplicity
        for (let i = 0; i < stateVector.length; i++) {
            const bit = (i >> qubit) & 1;
            if (bit === 1) {
                // Apply -i phase to |1⟩ states
                // Since we're using real numbers, we'll track phase separately
                // For now, just apply a sign change to simulate the effect
                stateVector[i] *= -1;
            }
        }
    }

    // Pauli-Z gate implementation
    applyPauliZ(stateVector, qubit, numQubits) {
        for (let i = 0; i < stateVector.length; i++) {
            const bit = (i >> qubit) & 1;
            if (bit === 1) {
                stateVector[i] *= -1;
            }
        }
    }

    // CNOT gate implementation
    applyCNOT(stateVector, control, target, numQubits) {
        const newState = new Array(stateVector.length).fill(0);

        for (let i = 0; i < stateVector.length; i++) {
            const controlBit = (i >> control) & 1;
            if (controlBit === 1) {
                const flippedTarget = i ^ (1 << target);
                newState[flippedTarget] = stateVector[i];
            } else {
                newState[i] = stateVector[i];
            }
        }

        // Copy back to original array
        for (let i = 0; i < stateVector.length; i++) {
            stateVector[i] = newState[i];
        }
    }

    // Measurement implementation
    applyMeasurement(qubit, circuit) {
        // Simplified measurement - collapse to random outcome based on probabilities
        const probabilities = this.getProbabilities(circuit.stateVector);
        const random = Math.random();
        let cumulative = 0;
        let outcome = 0;

        for (let i = 0; i < probabilities.length; i++) {
            cumulative += probabilities[i];
            if (random <= cumulative) {
                outcome = i;
                break;
            }
        }

        const measurement = {
            qubit: qubit,
            outcome: (outcome >> qubit) & 1,
            probability: probabilities[outcome],
            timestamp: Date.now()
        };

        circuit.measurements.push(measurement);
        this.collapseState(circuit.stateVector, outcome);
    }

    // Get measurement probabilities
    getProbabilities(stateVector) {
        return stateVector.map(amplitude => {
            // Handle complex numbers (simplified)
            if (typeof amplitude === 'object' && amplitude.imag) {
                return amplitude.real * amplitude.real + amplitude.imag * amplitude.imag;
            }
            return amplitude * amplitude;
        });
    }

    // Collapse quantum state after measurement
    collapseState(stateVector, outcome) {
        for (let i = 0; i < stateVector.length; i++) {
            stateVector[i] = i === outcome ? 1 : 0;
        }
    }

    // Run circuit simulation
    async run(shots = 1024) {
        if (!this.currentCircuit) {
            throw new Error('No active circuit');
        }

        const results = {
            counts: {},
            memory: [],
            shots: shots,
            success: true
        };

        // Simulate multiple shots
        for (let shot = 0; shot < shots; shot++) {
            // Reset state vector for each shot
            const originalState = [...this.currentCircuit.stateVector];
            this.currentCircuit.stateVector = this.initializeStateVector(this.currentCircuit.numQubits);

            // Apply all gates
            this.currentCircuit.gates.forEach(gate => {
                this.updateStateVector(gate);
            });

            // Get measurement outcomes
            const outcome = this.getMeasurementOutcome();
            const binaryString = outcome.toString(2).padStart(this.currentCircuit.numQubits, '0');

            results.counts[binaryString] = (results.counts[binaryString] || 0) + 1;
            results.memory.push(binaryString);

            // Restore original state
            this.currentCircuit.stateVector = originalState;
        }

        this.results.set(this.currentCircuit.id, results);
        return results;
    }

    // Get measurement outcome from current state
    getMeasurementOutcome() {
        const probabilities = this.getProbabilities(this.currentCircuit.stateVector);
        const random = Math.random();
        let cumulative = 0;
        let outcome = 0;

        for (let i = 0; i < probabilities.length; i++) {
            cumulative += probabilities[i];
            if (random <= cumulative) {
                outcome = i;
                break;
            }
        }

        return outcome;
    }

    // Get circuit information
    getCircuitInfo() {
        if (!this.currentCircuit) return null;

        return {
            id: this.currentCircuit.id,
            numQubits: this.currentCircuit.numQubits,
            numClassicalBits: this.currentCircuit.numClassicalBits,
            gateCount: this.currentCircuit.gates.length,
            measurements: this.currentCircuit.measurements.length,
            depth: this.calculateDepth()
        };
    }

    // Calculate circuit depth
    calculateDepth() {
        if (!this.currentCircuit) return 0;

        const qubitLastUsed = new Array(this.currentCircuit.numQubits).fill(-1);
        let maxDepth = 0;

        this.currentCircuit.gates.forEach((gate, index) => {
            const lastUse = qubitLastUsed[gate.qubit];
            const depth = lastUse + 1;
            qubitLastUsed[gate.qubit] = depth;
            maxDepth = Math.max(maxDepth, depth);
        });

        return maxDepth + 1;
    }

    // Reset circuit
    reset() {
        if (this.currentCircuit) {
            this.currentCircuit.gates = [];
            this.currentCircuit.measurements = [];
            this.currentCircuit.stateVector = this.initializeStateVector(this.currentCircuit.numQubits);
        }
    }

    // Export circuit to QASM format
    toQASM() {
        if (!this.currentCircuit) return '';

        let qasm = `OPENQASM 2.0;\n`;
        qasm += `include "qelib1.inc";\n\n`;
        qasm += `qreg q[${this.currentCircuit.numQubits}];\n`;
        qasm += `creg c[${this.currentCircuit.numClassicalBits}];\n\n`;

        this.currentCircuit.gates.forEach(gate => {
            switch (gate.type.toUpperCase()) {
                case 'H':
                    qasm += `h q[${gate.qubit}];\n`;
                    break;
                case 'X':
                    qasm += `x q[${gate.qubit}];\n`;
                    break;
                case 'Y':
                    qasm += `y q[${gate.qubit}];\n`;
                    break;
                case 'Z':
                    qasm += `z q[${gate.qubit}];\n`;
                    break;
                case 'CNOT':
                    qasm += `cx q[${gate.control}], q[${gate.qubit}];\n`;
                    break;
                case 'MEASURE':
                    qasm += `measure q[${gate.qubit}] -> c[${gate.qubit}];\n`;
                    break;
            }
        });

        return qasm;
    }

    // Get state vector as complex amplitudes
    getStateVector() {
        return this.currentCircuit ? [...this.currentCircuit.stateVector] : [];
    }

    // Get probability distribution
    getProbabilities() {
        return this.currentCircuit ? this.getProbabilities(this.currentCircuit.stateVector) : [];
    }
}

// Create global instance
window.qiskit = {
    QuantumCircuit: function(numQubits, numClassicalBits) {
        return window.quantumSimulator.createCircuit(numQubits, numClassicalBits);
    }
};

// Initialize global simulator
window.quantumSimulator = new QuantumSimulator();

// Add complex number support (simplified)
if (!window.Complex) {
    window.Complex = function(real, imag) {
        this.real = real || 0;
        this.imag = imag || 0;
    };

    window.Complex.prototype.toString = function() {
        if (this.imag === 0) return this.real.toString();
        if (this.real === 0) return this.imag + 'i';
        return this.real + (this.imag > 0 ? '+' : '') + this.imag + 'i';
    };
}
