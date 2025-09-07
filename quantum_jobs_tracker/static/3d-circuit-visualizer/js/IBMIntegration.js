// IBM Quantum Integration - API connectivity and device management
// Handles authentication, job submission, and real device interactions

class IBMIntegration {
    constructor() {
        this.token = null;
        this.isAuthenticated = false;
        this.devices = [];
        this.currentJob = null;
        this.jobHistory = [];
        this.backend = null;

        // IBM Quantum API configuration
        this.apiBaseUrl = 'https://api.quantum-computing.ibm.com/api';
        this.authUrl = 'https://auth.quantum-computing.ibm.com/api';
    }

    async connect(token) {
        if (!token) {
            throw new Error('IBM Quantum token is required');
        }

        this.token = token;

        try {
            // Validate token by attempting to get user info
            const response = await this.makeAuthenticatedRequest('/users/me');

            if (response.ok) {
                this.isAuthenticated = true;
                console.log('Successfully connected to IBM Quantum');

                // Load available devices
                await this.loadDevices();
            } else {
                throw new Error('Invalid IBM Quantum token');
            }
        } catch (error) {
            this.isAuthenticated = false;
            console.error('IBM Quantum connection failed:', error);
            throw error;
        }
    }

    async makeAuthenticatedRequest(endpoint, options = {}) {
        const url = `${this.apiBaseUrl}${endpoint}`;
        const headers = {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json',
            ...options.headers
        };

        const requestOptions = {
            ...options,
            headers
        };

        return await fetch(url, requestOptions);
    }

    async loadDevices() {
        try {
            const response = await this.makeAuthenticatedRequest('/backends');

            if (!response.ok) {
                throw new Error(`Failed to load devices: ${response.status}`);
            }

            const data = await response.json();
            this.devices = data.backends || [];

            console.log(`Loaded ${this.devices.length} IBM Quantum devices`);
        } catch (error) {
            console.error('Failed to load devices:', error);
            throw error;
        }
    }

    async getDevices() {
        if (!this.isAuthenticated) {
            throw new Error('Not authenticated with IBM Quantum');
        }

        if (this.devices.length === 0) {
            await this.loadDevices();
        }

        return this.devices.map(device => ({
            id: device.backend_name,
            name: device.backend_name,
            status: device.backend_status || 'unknown',
            queue: device.queue_length || 0,
            qubits: device.n_qubits || 0,
            simulator: device.simulator || false,
            description: device.description || '',
            coupling_map: device.coupling_map || [],
            basis_gates: device.basis_gates || []
        }));
    }

    async selectBackend(backendName) {
        const devices = await this.getDevices();
        const device = devices.find(d => d.name === backendName);

        if (!device) {
            throw new Error(`Backend ${backendName} not found`);
        }

        this.backend = device;
        console.log(`Selected backend: ${backendName}`);

        return device;
    }

    async submitJob(circuit, shots = 1024, optimizationLevel = 1) {
        if (!this.isAuthenticated) {
            throw new Error('Not authenticated with IBM Quantum');
        }

        if (!this.backend) {
            throw new Error('No backend selected');
        }

        try {
            // Convert circuit to QASM format
            const qasmCircuit = this.convertCircuitToQASM(circuit);

            const jobData = {
                backend: this.backend.name,
                qasm: qasmCircuit,
                shots: shots,
                optimization_level: optimizationLevel,
                seed: Math.floor(Math.random() * 1000000)
            };

            const response = await this.makeAuthenticatedRequest('/jobs', {
                method: 'POST',
                body: JSON.stringify(jobData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Job submission failed: ${errorData.error}`);
            }

            const jobResult = await response.json();
            this.currentJob = {
                id: jobResult.id,
                backend: this.backend.name,
                status: 'queued',
                submittedAt: new Date(),
                shots: shots
            };

            this.jobHistory.push(this.currentJob);

            console.log(`Job submitted successfully: ${jobResult.id}`);
            return this.currentJob;
        } catch (error) {
            console.error('Job submission failed:', error);
            throw error;
        }
    }

    async getJobStatus(jobId = null) {
        const id = jobId || (this.currentJob && this.currentJob.id);

        if (!id) {
            throw new Error('No job ID available');
        }

        try {
            const response = await this.makeAuthenticatedRequest(`/jobs/${id}`);

            if (!response.ok) {
                throw new Error(`Failed to get job status: ${response.status}`);
            }

            const jobData = await response.json();

            // Update current job status
            if (this.currentJob && this.currentJob.id === id) {
                this.currentJob.status = jobData.status;
                this.currentJob.completedAt = jobData.status === 'completed' ? new Date() : null;
            }

            return {
                id: jobData.id,
                status: jobData.status,
                backend: jobData.backend,
                submittedAt: jobData.creation_date,
                completedAt: jobData.end_date,
                queuePosition: jobData.queue_position,
                estimatedTime: jobData.estimated_start_time
            };
        } catch (error) {
            console.error('Failed to get job status:', error);
            throw error;
        }
    }

    async getJobResults(jobId = null) {
        const id = jobId || (this.currentJob && this.currentJob.id);

        if (!id) {
            throw new Error('No job ID available');
        }

        try {
            const response = await this.makeAuthenticatedRequest(`/jobs/${id}/results`);

            if (!response.ok) {
                throw new Error(`Failed to get job results: ${response.status}`);
            }

            const resultsData = await response.json();

            // Process results
            const processedResults = this.processJobResults(resultsData);

            return processedResults;
        } catch (error) {
            console.error('Failed to get job results:', error);
            throw error;
        }
    }

    processJobResults(resultsData) {
        if (!resultsData.results || resultsData.results.length === 0) {
            return null;
        }

        const result = resultsData.results[0];
        const counts = {};

        // Convert IBM result format to standard format
        if (result.data && result.data.counts) {
            Object.entries(result.data.counts).forEach(([key, value]) => {
                counts[key] = value;
            });
        }

        return {
            counts: counts,
            shots: result.shots,
            success: result.success,
            time_taken: result.time_taken,
            header: result.header
        };
    }

    async cancelJob(jobId = null) {
        const id = jobId || (this.currentJob && this.currentJob.id);

        if (!id) {
            throw new Error('No job ID available');
        }

        try {
            const response = await this.makeAuthenticatedRequest(`/jobs/${id}/cancel`, {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error(`Failed to cancel job: ${response.status}`);
            }

            if (this.currentJob && this.currentJob.id === id) {
                this.currentJob.status = 'cancelled';
            }

            console.log(`Job ${id} cancelled successfully`);
        } catch (error) {
            console.error('Failed to cancel job:', error);
            throw error;
        }
    }

    async getJobHistory(limit = 10) {
        try {
            const response = await this.makeAuthenticatedRequest(`/jobs?limit=${limit}`);

            if (!response.ok) {
                throw new Error(`Failed to get job history: ${response.status}`);
            }

            const historyData = await response.json();
            return historyData.jobs || [];
        } catch (error) {
            console.error('Failed to get job history:', error);
            throw error;
        }
    }

    convertCircuitToQASM(circuit) {
        // Convert quantum circuit to QASM format
        // This is a simplified implementation - in production you'd use Qiskit's QASM export
        let qasm = `OPENQASM 2.0;\n`;
        qasm += `include "qelib1.inc";\n\n`;

        qasm += `qreg q[${circuit.numQubits}];\n`;
        qasm += `creg c[${circuit.numClassicalBits || circuit.numQubits}];\n\n`;

        // Add gates from circuit
        circuit.gates.forEach(gate => {
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

    // Utility methods
    isConnected() {
        return this.isAuthenticated;
    }

    getCurrentBackend() {
        return this.backend;
    }

    getCurrentJob() {
        return this.currentJob;
    }

    disconnect() {
        this.token = null;
        this.isAuthenticated = false;
        this.devices = [];
        this.backend = null;
        this.currentJob = null;
        console.log('Disconnected from IBM Quantum');
    }

    // Error handling and retry logic
    async retryOperation(operation, maxRetries = 3, delay = 1000) {
        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                return await operation();
            } catch (error) {
                if (attempt === maxRetries) {
                    throw error;
                }

                console.warn(`Operation failed (attempt ${attempt}/${maxRetries}), retrying...`);
                await new Promise(resolve => setTimeout(resolve, delay * attempt));
            }
        }
    }

    // Device information and calibration data
    async getDeviceCalibration(backendName) {
        try {
            const response = await this.makeAuthenticatedRequest(`/backends/${backendName}/calibration`);

            if (!response.ok) {
                throw new Error(`Failed to get calibration data: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Failed to get device calibration:', error);
            throw error;
        }
    }

    async getDeviceProperties(backendName) {
        try {
            const response = await this.makeAuthenticatedRequest(`/backends/${backendName}/properties`);

            if (!response.ok) {
                throw new Error(`Failed to get device properties: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Failed to get device properties:', error);
            throw error;
        }
    }

    // Batch job operations
    async submitBatchJobs(jobs) {
        const batchPromises = jobs.map(job =>
            this.retryOperation(() => this.submitJob(job.circuit, job.shots, job.optimizationLevel))
        );

        try {
            const results = await Promise.allSettled(batchPromises);
            return results.map((result, index) => ({
                job: jobs[index],
                success: result.status === 'fulfilled',
                data: result.value,
                error: result.reason
            }));
        } catch (error) {
            console.error('Batch job submission failed:', error);
            throw error;
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = IBMIntegration;
}
