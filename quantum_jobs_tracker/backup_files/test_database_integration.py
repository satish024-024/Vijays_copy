#!/usr/bin/env python3
"""
Test script for database integration
Tests the database functionality and data persistence
"""

import sys
import os
import time
import json
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import db

def test_database_creation():
    """Test database creation and table initialization"""
    print("🧪 Testing database creation...")
    
    try:
        # Test database stats
        stats = db.get_database_stats()
        print(f"✅ Database created successfully")
        print(f"   - Backends: {stats.get('backends_count', 0)} records")
        print(f"   - Jobs: {stats.get('jobs_count', 0)} records")
        print(f"   - Metrics: {stats.get('metrics_count', 0)} records")
        print(f"   - Quantum States: {stats.get('quantum_states_count', 0)} records")
        print(f"   - Database Size: {stats.get('database_size_bytes', 0) / 1024:.2f} KB")
        return True
    except Exception as e:
        print(f"❌ Database creation failed: {e}")
        return False

def test_data_storage():
    """Test storing sample data"""
    print("\n🧪 Testing data storage...")
    
    try:
        # Test backends storage
        sample_backends = [
            {
                "name": "ibmq_qasm_simulator",
                "status": "active",
                "qubits": 32,
                "operational": True,
                "pending_jobs": 5,
                "max_experiments": 100,
                "max_shots": 100000
            },
            {
                "name": "ibmq_lima",
                "status": "active", 
                "qubits": 5,
                "operational": True,
                "pending_jobs": 12,
                "max_experiments": 75,
                "max_shots": 8192
            }
        ]
        
        db.store_backends(sample_backends)
        print(" Backends stored successfully")
        
        # Test jobs storage
        sample_jobs = [
            {
                "job_id": "test_job_001",
                "backend_name": "ibmq_qasm_simulator",
                "status": "completed",
                "creation_date": datetime.now().isoformat(),
                "end_date": (datetime.now() + timedelta(minutes=5)).isoformat(),
                "queue_position": 0,
                "estimated_time": "2 minutes",
                "shots": 1024
            },
            {
                "job_id": "test_job_002", 
                "backend_name": "ibmq_lima",
                "status": "running",
                "creation_date": datetime.now().isoformat(),
                "queue_position": 3,
                "estimated_time": "5 minutes",
                "shots": 2048
            }
        ]
        
        db.store_jobs(sample_jobs)
        print("✅ Jobs stored successfully")
        
        # Test metrics storage
        sample_metrics = {
            "active_backends": 2,
            "total_jobs": 2,
            "running_jobs": 1,
            "success_rate": 0.95
        }
        
        db.store_metrics(sample_metrics)
        print("✅ Metrics stored successfully")
        
        # Test quantum state storage
        sample_state = {
            "name": "test_state",
            "state_vector": [0.707, 0.707, 0],
            "theta": 1.57,
            "phi": 0.0,
            "fidelity": 0.98
        }
        
        db.store_quantum_state(sample_state)
        print("✅ Quantum state stored successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Data storage failed: {e}")
        return False

def test_data_retrieval():
    """Test retrieving stored data"""
    print("\n🧪 Testing data retrieval...")
    
    try:
        # Test getting latest data
        latest_data = db.get_latest_data(hours_back=1)
        print(f"✅ Latest data retrieved:")
        print(f"   - Backends: {len(latest_data.get('backends', []))}")
        print(f"   - Jobs: {len(latest_data.get('jobs', []))}")
        print(f"   - Metrics: {len(latest_data.get('metrics', []))}")
        print(f"   - Quantum States: {len(latest_data.get('quantum_states', []))}")
        
        # Test getting offline data
        offline_data = db.get_offline_data()
        print(f"✅ Offline data retrieved:")
        print(f"   - Backends: {len(offline_data.get('backends', []))}")
        print(f"   - Jobs: {len(offline_data.get('jobs', []))}")
        print(f"   - Metrics: {len(offline_data.get('metrics', []))}")
        
        # Test getting historical metrics
        metrics_history = db.get_historical_metrics('active_backends', hours_back=1)
        print(f"✅ Metrics history retrieved: {len(metrics_history)} data points")
        
        return True
        
    except Exception as e:
        print(f"❌ Data retrieval failed: {e}")
        return False

def test_system_status():
    """Test system status tracking"""
    print("\n🧪 Testing system status...")
    
    try:
        # Test online status
        db.update_system_status(True)
        print("✅ Online status updated")
        
        # Test offline status with error
        db.update_system_status(False, "Test error message")
        print("✅ Offline status updated")
        
        return True
        
    except Exception as e:
        print(f"❌ System status test failed: {e}")
        return False

def test_data_cleanup():
    """Test data cleanup functionality"""
    print("\n🧪 Testing data cleanup...")
    
    try:
        # Get stats before cleanup
        stats_before = db.get_database_stats()
        print(f"   - Records before cleanup: {stats_before.get('backends_count', 0) + stats_before.get('jobs_count', 0)}")
        
        # Clean up data older than 0 days (should clean everything)
        db.cleanup_old_data(days_to_keep=0)
        
        # Get stats after cleanup
        stats_after = db.get_database_stats()
        print(f"   - Records after cleanup: {stats_after.get('backends_count', 0) + stats_after.get('jobs_count', 0)}")
        
        print("✅ Data cleanup completed")
        return True
        
    except Exception as e:
        print(f"❌ Data cleanup failed: {e}")
        return False

def main():
    """Run all database tests"""
    print("🚀 Starting Database Integration Tests")
    print("=" * 50)
    
    tests = [
        test_database_creation,
        test_data_storage,
        test_data_retrieval,
        test_system_status,
        test_data_cleanup
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Database integration is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
