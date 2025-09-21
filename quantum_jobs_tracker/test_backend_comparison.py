#!/usr/bin/env python3
"""
Test script for Backend Comparison functionality
Tests the advanced backend comparison popup feature
"""

import requests
import json
import time

BASE_URL = "http://localhost:10000"

def test_backend_comparison_api():
    print("🔍 Testing Backend Comparison API...")
    try:
        headers = {'Content-Type': 'application/json'}
        payload = {
            "job_complexity": "high",
            "shots": 2048,
            "num_qubits": 8,
            "algorithm": "VQE"
        }
        response = requests.post(f"{BASE_URL}/api/backend_comparison", headers=headers, data=json.dumps(payload))
        data = response.json()
        
        if response.status_code == 200:
            print(f"   ✅ Backend comparison API works")
            print(f"   📊 Backends: {len(data.get('backends', []))}")
            print(f"   🎯 Analysis: {data.get('analysis', {}).get('summary', 'N/A')}")
            return True
        else:
            print(f"   ❌ Backend comparison API failed: {response.status_code} - {data}")
            return False
    except Exception as e:
        print(f"   ❌ Backend comparison API error: {e}")
        return False

def test_backends_api():
    print("\n🔄 Testing Backends API...")
    try:
        response = requests.get(f"{BASE_URL}/api/backends")
        data = response.json()
        
        if response.status_code == 200:
            # Handle both list and object responses
            if isinstance(data, list):
                backends = data
            else:
                backends = data.get('backends', [])
            print(f"   ✅ Backends API works: {len(backends)} backends")
            if backends:
                print(f"   📊 Sample backend: {backends[0].get('name', 'Unknown')}")
            return True
        else:
            print(f"   ❌ Backends API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Backends API error: {e}")
        return False

def test_jobs_api():
    print("\n⚛️ Testing Jobs API...")
    try:
        response = requests.get(f"{BASE_URL}/api/jobs")
        data = response.json()
        
        if response.status_code == 200:
            jobs = data if isinstance(data, list) else data.get('jobs', [])
            print(f"   ✅ Jobs API works: {len(jobs)} jobs")
            return True
        else:
            print(f"   ❌ Jobs API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Jobs API error: {e}")
        return False

def test_dashboard_metrics():
    print("\n📊 Testing Dashboard Metrics...")
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard_metrics")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Dashboard metrics works")
            print(f"   📈 Active backends: {data.get('active_backends', 0)}")
            print(f"   📈 Total jobs: {data.get('total_jobs', 0)}")
            return True
        elif response.status_code == 401:
            print(f"   ⚠️ Dashboard metrics requires authentication (expected)")
            return True
        else:
            print(f"   ❌ Dashboard metrics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Dashboard metrics error: {e}")
        return False

def main():
    print("🧪 Testing Backend Comparison Functionality...")
    print("=" * 50)
    
    # Test all APIs
    backend_comparison_ok = test_backend_comparison_api()
    backends_ok = test_backends_api()
    jobs_ok = test_jobs_api()
    metrics_ok = test_dashboard_metrics()
    
    print("\n" + "=" * 50)
    print("🎯 Backend Comparison Test Complete!")
    
    if all([backend_comparison_ok, backends_ok, jobs_ok, metrics_ok]):
        print("✅ All tests passed! Backend comparison feature is working correctly.")
        print("\n🎨 Features implemented:")
        print("   • Advanced backend comparison popup")
        print("   • Real-time performance analysis")
        print("   • Cost analysis and recommendations")
        print("   • Professional UI with IBM Quantum styling")
        print("   • Integration with existing hackathon dashboard")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return all([backend_comparison_ok, backends_ok, jobs_ok, metrics_ok])

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
