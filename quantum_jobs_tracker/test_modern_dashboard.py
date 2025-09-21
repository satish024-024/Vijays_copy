#!/usr/bin/env python3
"""
Test script for Modern Dashboard API endpoints
This script tests all the API endpoints that the modern dashboard uses
"""

import requests
import json
import sys
import time

def test_api_endpoint(url, endpoint_name):
    """Test a single API endpoint"""
    try:
        print(f"Testing {endpoint_name}...")
        response = requests.get(f"{url}{endpoint_name}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {endpoint_name}: OK (Status: {response.status_code})")
            print(f"   Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            if 'real_data' in data:
                print(f"   Real data: {data['real_data']}")
            return True
        else:
            print(f"❌ {endpoint_name}: FAILED (Status: {response.status_code})")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {endpoint_name}: ERROR - {str(e)}")
        return False
    except Exception as e:
        print(f"❌ {endpoint_name}: ERROR - {str(e)}")
        return False

def main():
    """Test all modern dashboard API endpoints"""
    base_url = "http://localhost:5000"
    
    # List of API endpoints used by modern dashboard
    endpoints = [
        "/api/backends",
        "/api/jobs", 
        "/api/performance_metrics",
        "/api/realtime_monitoring",
        "/api/circuit_details",
        "/api/historical_data",
        "/api/calibration_data",
        "/api/dashboard_metrics"
    ]
    
    print("🧪 Testing Modern Dashboard API Endpoints")
    print("=" * 50)
    
    # Test if server is running
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server returned status {response.status_code}")
            return
    except requests.exceptions.RequestException:
        print("❌ Server is not running. Please start the server first.")
        print("   Run: python real_quantum_app.py")
        return
    
    print()
    
    # Test each endpoint
    results = []
    for endpoint in endpoints:
        success = test_api_endpoint(base_url, endpoint)
        results.append((endpoint, success))
        time.sleep(0.5)  # Small delay between requests
        print()
    
    # Summary
    print("📊 Test Results Summary")
    print("=" * 30)
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for endpoint, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {endpoint}")
    
    print(f"\nOverall: {passed}/{total} endpoints working")
    
    if passed == total:
        print("🎉 All API endpoints are working! Modern dashboard should load properly.")
    else:
        print("⚠️  Some API endpoints are not working. Check server logs for details.")
        print("   Make sure you have IBM Quantum credentials configured.")

if __name__ == "__main__":
    main()
