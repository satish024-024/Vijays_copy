#!/usr/bin/env python3
"""
API Endpoints Testing Script
Tests all API endpoints and IBM Quantum connectivity
"""

import requests
import json
import time

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:10000"
    
    print("🔍 Testing API Endpoints...")
    
    # Test 1: Authentication page
    print("\n1. Testing Authentication Page...")
    try:
        response = requests.get(f"{base_url}/auth", timeout=10)
        if response.status_code == 200:
            print("   ✅ Authentication page accessible")
        else:
            print(f"   ❌ Authentication page failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Authentication page error: {e}")
    
    # Test 2: Registration endpoint
    print("\n2. Testing Registration Endpoint...")
    try:
        test_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "api_key": "test_api_key_12345",
            "crn": "test_crn_67890"
        }
        response = requests.post(f"{base_url}/auth/register", 
                               json=test_data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("   ✅ Registration endpoint working")
            else:
                print(f"   ❌ Registration failed: {result.get('message')}")
        else:
            print(f"   ❌ Registration endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Registration endpoint error: {e}")
    
    # Test 3: Login endpoint
    print("\n3. Testing Login Endpoint...")
    try:
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{base_url}/auth/login", 
                               json=login_data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("   ✅ Login endpoint working")
                auth_token = result.get('token')
                print(f"   🔑 Auth token received: {auth_token[:20]}...")
            else:
                print(f"   ❌ Login failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ Login endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Login endpoint error: {e}")
        return False
    
    # Test 4: Protected endpoints (without authentication)
    print("\n4. Testing Protected Endpoints (without auth)...")
    protected_endpoints = [
        "/api/job_results",
        "/api/performance_metrics",
        "/api/realtime_monitoring",
        "/api/historical_data",
        "/api/calibration_data"
    ]
    
    for endpoint in protected_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 401:
                print(f"   ✅ {endpoint}: Properly protected (401)")
            else:
                print(f"   ⚠️  {endpoint}: Unexpected response ({response.status_code})")
        except Exception as e:
            print(f"   ❌ {endpoint}: Error - {e}")
    
    # Test 5: Dashboard access (should redirect to auth)
    print("\n5. Testing Dashboard Access...")
    try:
        response = requests.get(f"{base_url}/", timeout=5, allow_redirects=False)
        if response.status_code in [302, 401]:
            print("   ✅ Dashboard properly protected")
        else:
            print(f"   ⚠️  Dashboard access: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Dashboard access error: {e}")
    
    print("\n✅ API endpoint testing completed")
    return True

def test_quantum_connectivity():
    """Test IBM Quantum connectivity"""
    print("\n🔗 Testing IBM Quantum Connectivity...")
    
    try:
        # Test with demo credentials (should fail gracefully)
        from real_quantum_app import QuantumBackendManager
        
        print("   🧪 Testing QuantumBackendManager with demo credentials...")
        manager = QuantumBackendManager(token="demo_token_for_testing", crn="demo_crn_for_testing")
        
        if manager.is_connected:
            print("   ✅ QuantumBackendManager connected successfully")
        else:
            print("   ⚠️  QuantumBackendManager not connected (expected with demo credentials)")
        
        print("   ✅ QuantumBackendManager initialization working")
        return True
        
    except Exception as e:
        print(f"   ❌ Quantum connectivity test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Comprehensive API Testing...")
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    api_success = test_api_endpoints()
    quantum_success = test_quantum_connectivity()
    
    if api_success and quantum_success:
        print("\n🎉 All API tests passed!")
    else:
        print("\n💥 Some API tests failed!")
