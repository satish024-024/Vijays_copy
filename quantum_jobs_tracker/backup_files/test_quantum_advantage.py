#!/usr/bin/env python3
"""
Test script for Quantum Advantage Research Platform
Verifies all components are working correctly
"""

import sys
import os
import time
import numpy as np

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_platform_import():
    """Test importing the main platform"""
    print("🔬 Testing Quantum Advantage Platform imports...")

    try:
        from quantum_advantage_platform import QuantumAdvantagePlatform
        from quantum_algorithms import MolecularVQE, QAOAOptimizer, QuantumMLPlatform
        from backend_optimizer import QuantumBackendOptimizer
        from transpiler_optimizer import QuantumTranspilerOptimizer
        from scientific_visualizations import QuantumAdvantageVisualizer, QuantumExperimentReport

        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_platform_initialization():
    """Test platform initialization"""
    print("\n🏗️ Testing platform initialization...")

    try:
        from quantum_advantage_platform import QuantumAdvantagePlatform

        platform = QuantumAdvantagePlatform()
        print("✅ Platform initialized successfully")
        print(f"   - VQE Suite: {'✅' if platform.vqe_suite else '❌'}")
        print(f"   - QAOA Suite: {'✅' if platform.qaoa_suite else '❌'}")
        print(f"   - QML Suite: {'✅' if platform.qml_suite else '❌'}")
        print(f"   - Backend Optimizer: {'✅' if platform.backend_optimizer else '❌'}")
        print(f"   - Transpiler Optimizer: {'✅' if platform.transpiler_optimizer else '❌'}")

        return True
    except Exception as e:
        print(f"❌ Platform initialization failed: {e}")
        return False

def test_algorithm_creation():
    """Test quantum algorithm creation"""
    print("\n🧬 Testing quantum algorithm creation...")

    try:
        from quantum_algorithms import MolecularVQE, QAOAOptimizer, QuantumMLPlatform

        # Test VQE
        vqe = MolecularVQE()
        circuit = vqe.create_vqe_circuit(4)
        print(f"✅ VQE circuit created: {circuit.num_qubits} qubits, {circuit.depth()} depth")

        # Test QAOA
        qaoa = QAOAOptimizer()
        circuit = qaoa.create_qaoa_circuit(4)
        print(f"✅ QAOA circuit created: {circuit.num_qubits} qubits, {circuit.depth()} depth")

        # Test QML
        qml = QuantumMLPlatform()
        circuit = qml.create_qml_circuit(4)
        print(f"✅ QML circuit created: {circuit.num_qubits} qubits, {circuit.depth()} depth")

        return True
    except Exception as e:
        print(f"❌ Algorithm creation failed: {e}")
        return False

def test_backend_optimizer():
    """Test backend optimizer"""
    print("\n🎯 Testing backend optimizer...")

    try:
        from backend_optimizer import QuantumBackendOptimizer

        optimizer = QuantumBackendOptimizer()
        backends = optimizer._get_available_backends()
        print(f"✅ Found {len(backends)} available backends")

        # Test backend selection
        mock_circuit = type('MockCircuit', (), {'num_qubits': 5, 'depth': lambda self: 10, 'data': []})()
        selection = optimizer.select_optimal_backend(mock_circuit, {'max_queue_time': 600})
        print(f"✅ Backend selection: {selection.get('optimal_backend', 'None')}")

        return True
    except Exception as e:
        print(f"❌ Backend optimizer test failed: {e}")
        return False

def test_visualizations():
    """Test visualization creation"""
    print("\n📊 Testing visualization creation...")

    try:
        from scientific_visualizations import QuantumAdvantageVisualizer

        visualizer = QuantumAdvantageVisualizer()

        # Test advantage landscape
        mock_data = {
            'problem_sizes': [5, 10, 15],
            'quantum_results': [
                {'runtime': 0.1, 'error_metrics': {'total_error': 0.1}},
                {'runtime': 0.5, 'error_metrics': {'total_error': 0.15}},
                {'runtime': 2.0, 'error_metrics': {'total_error': 0.2}}
            ],
            'classical_results': [
                {'runtime': 0.2},
                {'runtime': 1.0},
                {'runtime': 4.0}
            ]
        }

        landscape = visualizer.create_advantage_landscape(mock_data)
        print(f"✅ Advantage landscape created: {type(landscape)}")

        return True
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        return False

def test_experiment_reporting():
    """Test experiment reporting"""
    print("\n📄 Testing experiment reporting...")

    try:
        from scientific_visualizations import QuantumExperimentReport

        reporter = QuantumExperimentReport()

        mock_experiment = {
            'algorithm': 'vqe',
            'study_results': {
                'quantum_results': [{'runtime': 0.1}, {'runtime': 0.5}],
                'classical_results': [{'runtime': 0.2}, {'runtime': 1.0}],
                'advantage_analysis': {'quantum_advantage_detected': True, 'max_advantage_ratio': 2.0}
            },
            'advantage_detected': True,
            'max_advantage_ratio': 2.0
        }

        report = reporter.generate_research_report(mock_experiment)
        print(f"✅ Research report generated: {len(report)} sections")

        # Test different export formats
        json_report = reporter.export_report(report, 'json')
        html_report = reporter.export_report(report, 'html')
        print(f"✅ Report export formats: JSON ({len(json_report)} chars), HTML ({len(html_report)} chars)")

        return True
    except Exception as e:
        print(f"❌ Experiment reporting test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Quantum Advantage Research Platform - Test Suite")
    print("=" * 60)

    tests = [
        ("Platform Import", test_platform_import),
        ("Platform Initialization", test_platform_initialization),
        ("Algorithm Creation", test_algorithm_creation),
        ("Backend Optimizer", test_backend_optimizer),
        ("Visualizations", test_visualizations),
        ("Experiment Reporting", test_experiment_reporting)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Quantum Advantage Platform is ready!")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
