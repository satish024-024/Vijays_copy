"""
Quantum Backend Optimizer
ML-driven backend selection considering circuit-specific error rates, queue time, and cost
"""

import numpy as np
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os


class QuantumBackendOptimizer:
    """
    Intelligent Backend Selection with ML-driven optimization
    """

    def __init__(self):
        self.backend_performance_db = QuantumBackendDatabase()
        self.ml_predictor = BackendPerformancePredictor()
        self.available_backends = []
        self.performance_history = []

    def select_optimal_backend(self, circuit, requirements: Dict) -> Dict:
        """
        ML-driven backend selection considering:
        - Circuit-specific error rates
        - Queue time predictions
        - Cost optimization
        - Success probability estimation

        Args:
            circuit: Quantum circuit to optimize for
            requirements: Dict with keys like 'max_queue_time', 'min_fidelity', etc.

        Returns:
            Optimal backend selection with reasoning
        """
        print("🎯 Optimizing backend selection...")

        # Extract circuit features
        circuit_features = self._extract_circuit_features(circuit)

        # Get available backends (would be fetched from IBM Quantum in practice)
        if not self.available_backends:
            self.available_backends = self._get_available_backends()

        backend_scores = {}

        for backend in self.available_backends:
            # Get backend calibration data
            backend_calibration = self._get_backend_calibration(backend)

            # Get historical performance
            historical_performance = self.backend_performance_db.get_history(backend['name'])

            # Predict performance using ML model
            predicted_performance = self.ml_predictor.predict(
                circuit_features=circuit_features,
                backend_calibration=backend_calibration,
                historical_performance=historical_performance
            )

            backend_scores[backend['name']] = predicted_performance

        # Rank backends based on requirements
        ranked_backends = self.rank_backends(backend_scores, requirements)

        # Select optimal backend
        optimal_backend = ranked_backends[0] if ranked_backends else None

        result = {
            'optimal_backend': optimal_backend,
            'all_scores': backend_scores,
            'ranking_reasoning': self._generate_ranking_reasoning(ranked_backends, requirements),
            'expected_performance': backend_scores.get(optimal_backend, {}) if optimal_backend else {},
            'selection_timestamp': datetime.now().isoformat()
        }

        self.performance_history.append(result)
        return result

    def rank_backends(self, backend_scores: Dict, requirements: Dict) -> List[str]:
        """
        Rank backends based on requirements and predicted performance

        Args:
            backend_scores: Dict of backend names to performance predictions
            requirements: User requirements (queue_time, fidelity, cost, etc.)

        Returns:
            Ranked list of backend names (best first)
        """
        scored_backends = []

        for backend_name, scores in backend_scores.items():
            # Calculate composite score based on requirements
            composite_score = self._calculate_composite_score(scores, requirements)
            scored_backends.append((backend_name, composite_score))

        # Sort by composite score (higher is better)
        scored_backends.sort(key=lambda x: x[1], reverse=True)

        return [backend for backend, score in scored_backends]

    def _extract_circuit_features(self, circuit) -> Dict:
        """Extract features from quantum circuit for ML prediction"""
        features = {
            'num_qubits': circuit.num_qubits,
            'depth': circuit.depth(),
            'gate_count': sum(1 for _ in circuit.data),
            'two_qubit_gates': sum(1 for instr, _, _ in circuit.data if len(instr.qubits) == 2),
            'single_qubit_gates': sum(1 for instr, _, _ in circuit.data if len(instr.qubits) == 1),
            'measurement_count': sum(1 for instr, _, _ in circuit.data if instr.name == 'measure'),
            'entangling_gates_ratio': 0.0,
            'gate_density': 0.0,
            'circuit_complexity': 0.0
        }

        # Calculate ratios and complexity metrics
        total_gates = features['gate_count']
        if total_gates > 0:
            features['entangling_gates_ratio'] = features['two_qubit_gates'] / total_gates
            features['gate_density'] = total_gates / (features['num_qubits'] * features['depth'])
            features['circuit_complexity'] = features['depth'] * features['entangling_gates_ratio']

        return features

    def _get_available_backends(self) -> List[Dict]:
        """Get list of available IBM Quantum backends"""
        # In practice, this would query IBM Quantum API
        # For now, return mock backends
        return [
            {
                'name': 'ibm_kyoto',
                'n_qubits': 127,
                'basis_gates': ['cx', 'id', 'rz', 'sx', 'x'],
                'coupling_map': 'heavy_hex',
                'max_shots': 8192,
                'status': 'online'
            },
            {
                'name': 'ibm_osaka',
                'n_qubits': 127,
                'basis_gates': ['cx', 'id', 'rz', 'sx', 'x'],
                'coupling_map': 'heavy_hex',
                'max_shots': 8192,
                'status': 'online'
            },
            {
                'name': 'ibm_brisbane',
                'n_qubits': 127,
                'basis_gates': ['cx', 'id', 'rz', 'sx', 'x'],
                'coupling_map': 'heavy_hex',
                'max_shots': 8192,
                'status': 'online'
            },
            {
                'name': 'ibmq_qasm_simulator',
                'n_qubits': 32,
                'basis_gates': ['cx', 'id', 'rz', 'sx', 'x', 'u1', 'u2', 'u3'],
                'coupling_map': None,
                'max_shots': 8192,
                'status': 'online'
            }
        ]

    def _get_backend_calibration(self, backend: Dict) -> Dict:
        """Get current calibration data for backend"""
        # In practice, this would fetch real calibration data
        return {
            't1_times': np.random.uniform(50e-6, 200e-6, backend['n_qubits']),
            't2_times': np.random.uniform(30e-6, 150e-6, backend['n_qubits']),
            'gate_errors': np.random.uniform(0.001, 0.01, len(backend['basis_gates'])),
            'readout_errors': np.random.uniform(0.01, 0.05, backend['n_qubits']),
            'crosstalk_matrix': np.random.uniform(0.001, 0.005, (backend['n_qubits'], backend['n_qubits'])),
            'last_calibration': datetime.now().isoformat()
        }

    def _calculate_composite_score(self, scores: Dict, requirements: Dict) -> float:
        """Calculate composite score for backend ranking"""
        # Weights for different factors
        weights = {
            'predicted_fidelity': 0.4,
            'predicted_queue_time': -0.3,  # Negative because shorter queue is better
            'predicted_cost': -0.2,  # Negative because lower cost is better
            'success_probability': 0.1
        }

        composite_score = 0.0

        for factor, weight in weights.items():
            if factor in scores:
                # Normalize score to 0-1 range
                normalized_score = self._normalize_score(scores[factor], factor)
                composite_score += weight * normalized_score

        # Apply requirement-based adjustments
        composite_score = self._apply_requirements_adjustment(composite_score, scores, requirements)

        return composite_score

    def _normalize_score(self, score: float, factor: str) -> float:
        """Normalize different types of scores to 0-1 range"""
        if factor == 'predicted_fidelity':
            return min(1.0, max(0.0, score))  # Already 0-1
        elif factor == 'predicted_queue_time':
            # Assume queue times up to 24 hours = 86400 seconds
            return max(0.0, 1.0 - (score / 86400))
        elif factor == 'predicted_cost':
            # Assume costs up to $1.00
            return max(0.0, 1.0 - score)
        elif factor == 'success_probability':
            return min(1.0, max(0.0, score))
        else:
            return 0.5  # Default neutral score

    def _apply_requirements_adjustment(self, score: float, backend_scores: Dict, requirements: Dict) -> float:
        """Apply requirement-based adjustments to score"""
        adjusted_score = score

        # Check queue time requirement
        if 'max_queue_time' in requirements:
            predicted_queue = backend_scores.get('predicted_queue_time', float('inf'))
            if predicted_queue > requirements['max_queue_time']:
                adjusted_score -= 1.0  # Heavy penalty for exceeding queue time

        # Check minimum fidelity requirement
        if 'min_fidelity' in requirements:
            predicted_fidelity = backend_scores.get('predicted_fidelity', 0.0)
            if predicted_fidelity < requirements['min_fidelity']:
                adjusted_score -= 1.0  # Heavy penalty for insufficient fidelity

        # Check cost limit
        if 'max_cost' in requirements:
            predicted_cost = backend_scores.get('predicted_cost', float('inf'))
            if predicted_cost > requirements['max_cost']:
                adjusted_score -= 0.5  # Moderate penalty for exceeding cost

        return adjusted_score

    def _generate_ranking_reasoning(self, ranked_backends: List[str], requirements: Dict) -> str:
        """Generate human-readable reasoning for backend ranking"""
        if not ranked_backends:
            return "No backends available meeting requirements"

        reasoning = f"Selected {ranked_backends[0]} as optimal backend because:"

        # Add specific reasoning based on requirements
        if 'max_queue_time' in requirements:
            reasoning += f" queue time within {requirements['max_queue_time']}s limit,"

        if 'min_fidelity' in requirements:
            reasoning += f" fidelity meets {requirements['min_fidelity']*100:.1f}% minimum,"

        if 'max_cost' in requirements:
            reasoning += f" cost within ${requirements['max_cost']:.3f} limit,"

        reasoning += " and overall performance optimization."

        return reasoning


class BackendPerformancePredictor:
    """
    ML model for predicting backend performance based on circuit features
    """

    def __init__(self):
        self.model_path = 'backend_predictor_model.pkl'
        self.scaler_path = 'backend_scaler.pkl'
        self.model = None
        self.scaler = None
        self.is_trained = False

        # Try to load existing model
        self._load_model()

        # If no model exists, initialize with default predictions
        if not self.is_trained:
            print("⚠️  No trained backend predictor model found - using heuristic predictions")

    def predict(self, circuit_features: Dict, backend_calibration: Dict, historical_performance: Dict) -> Dict:
        """
        Predict backend performance for given circuit and backend

        Args:
            circuit_features: Features extracted from quantum circuit
            backend_calibration: Current backend calibration data
            historical_performance: Historical performance data

        Returns:
            Predicted performance metrics
        """
        if self.is_trained and self.model is not None:
            return self._ml_prediction(circuit_features, backend_calibration, historical_performance)
        else:
            return self._heuristic_prediction(circuit_features, backend_calibration, historical_performance)

    def _ml_prediction(self, circuit_features: Dict, backend_calibration: Dict, historical_performance: Dict) -> Dict:
        """Make prediction using trained ML model"""
        # Combine all features
        features = self._combine_features(circuit_features, backend_calibration, historical_performance)

        # Scale features
        features_scaled = self.scaler.transform([features])

        # Make prediction
        prediction = self.model.predict(features_scaled)[0]

        return {
            'predicted_fidelity': prediction[0],
            'predicted_queue_time': prediction[1],
            'predicted_cost': prediction[2],
            'success_probability': prediction[3],
            'prediction_method': 'ml_model'
        }

    def _heuristic_prediction(self, circuit_features: Dict, backend_calibration: Dict, historical_performance: Dict) -> Dict:
        """Make prediction using heuristic rules"""
        # Simple heuristic predictions based on circuit and backend characteristics

        # Fidelity prediction based on circuit complexity and backend errors
        base_fidelity = 0.8
        complexity_penalty = circuit_features.get('circuit_complexity', 0) * 0.1
        gate_error_penalty = np.mean(backend_calibration.get('gate_errors', [0.01])) * 10
        predicted_fidelity = max(0.1, base_fidelity - complexity_penalty - gate_error_penalty)

        # Queue time prediction based on backend popularity and circuit complexity
        base_queue_time = 300  # 5 minutes
        complexity_multiplier = 1 + circuit_features.get('circuit_complexity', 0)
        predicted_queue_time = base_queue_time * complexity_multiplier

        # Cost prediction based on circuit size and backend type
        base_cost = 0.01
        qubit_cost = circuit_features.get('num_qubits', 1) * 0.001
        predicted_cost = base_cost + qubit_cost

        # Success probability based on fidelity
        success_probability = predicted_fidelity * 0.9  # Slightly conservative

        return {
            'predicted_fidelity': predicted_fidelity,
            'predicted_queue_time': predicted_queue_time,
            'predicted_cost': predicted_cost,
            'success_probability': success_probability,
            'prediction_method': 'heuristic'
        }

    def _combine_features(self, circuit_features: Dict, backend_calibration: Dict, historical_performance: Dict) -> List[float]:
        """Combine all features into single feature vector"""
        features = []

        # Circuit features
        features.extend([
            circuit_features.get('num_qubits', 0),
            circuit_features.get('depth', 0),
            circuit_features.get('gate_count', 0),
            circuit_features.get('two_qubit_gates', 0),
            circuit_features.get('entangling_gates_ratio', 0),
            circuit_features.get('circuit_complexity', 0)
        ])

        # Backend calibration features
        features.extend([
            np.mean(backend_calibration.get('t1_times', [100e-6])),
            np.mean(backend_calibration.get('t2_times', [50e-6])),
            np.mean(backend_calibration.get('gate_errors', [0.01])),
            np.mean(backend_calibration.get('readout_errors', [0.03]))
        ])

        # Historical performance features
        features.extend([
            historical_performance.get('avg_fidelity', 0.7),
            historical_performance.get('avg_queue_time', 600),
            historical_performance.get('avg_cost', 0.02)
        ])

        return features

    def _load_model(self):
        """Load trained ML model if it exists"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                self.is_trained = True
                print("✅ Loaded trained backend predictor model")
            else:
                self.is_trained = False
        except Exception as e:
            print(f"⚠️  Failed to load backend predictor model: {e}")
            self.is_trained = False

    def train_model(self, training_data: List[Dict]):
        """
        Train the ML model on historical performance data

        Args:
            training_data: List of training examples with features and actual performance
        """
        print("🏋️  Training backend performance predictor model...")

        X = []  # Features
        y = []  # Targets (fidelity, queue_time, cost, success_prob)

        for example in training_data:
            features = self._combine_features(
                example['circuit_features'],
                example['backend_calibration'],
                example['historical_performance']
            )
            targets = [
                example['actual_fidelity'],
                example['actual_queue_time'],
                example['actual_cost'],
                example['actual_success_probability']
            ]

            X.append(features)
            y.append(targets)

        # Train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()

        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

        # Save model
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)

        self.is_trained = True
        print("✅ Backend predictor model trained and saved")


class QuantumBackendDatabase:
    """
    Database for storing and retrieving backend performance history
    """

    def __init__(self):
        self.performance_data = {}
        self.db_path = 'backend_performance_db.json'

        # Load existing data
        self._load_database()

    def get_history(self, backend_name: str) -> Dict:
        """Get historical performance data for backend"""
        if backend_name in self.performance_data:
            return self.performance_data[backend_name]
        else:
            # Return default values for new backends
            return {
                'avg_fidelity': 0.7,
                'avg_queue_time': 600,  # 10 minutes
                'avg_cost': 0.02,
                'total_jobs': 0,
                'last_updated': datetime.now().isoformat()
            }

    def update_performance(self, backend_name: str, job_result: Dict):
        """Update backend performance database with new job result"""
        if backend_name not in self.performance_data:
            self.performance_data[backend_name] = {
                'avg_fidelity': 0.7,
                'avg_queue_time': 600,
                'avg_cost': 0.02,
                'total_jobs': 0,
                'last_updated': datetime.now().isoformat()
            }

        # Update running averages
        current = self.performance_data[backend_name]
        total_jobs = current['total_jobs'] + 1
        alpha = 1.0 / total_jobs  # Learning rate

        current['avg_fidelity'] = (1 - alpha) * current['avg_fidelity'] + alpha * job_result.get('fidelity', 0.7)
        current['avg_queue_time'] = (1 - alpha) * current['avg_queue_time'] + alpha * job_result.get('queue_time', 600)
        current['avg_cost'] = (1 - alpha) * current['avg_cost'] + alpha * job_result.get('cost', 0.02)
        current['total_jobs'] = total_jobs
        current['last_updated'] = datetime.now().isoformat()

        # Save to disk
        self._save_database()

    def _load_database(self):
        """Load performance database from disk"""
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r') as f:
                    self.performance_data = json.load(f)
                print("✅ Loaded backend performance database")
        except Exception as e:
            print(f"⚠️  Failed to load backend performance database: {e}")
            self.performance_data = {}

    def _save_database(self):
        """Save performance database to disk"""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(self.performance_data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Failed to save backend performance database: {e}")
