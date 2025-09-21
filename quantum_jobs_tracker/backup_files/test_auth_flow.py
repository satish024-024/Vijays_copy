#!/usr/bin/env python3
"""
Authentication Flow Testing Script
Tests the complete authentication flow and data retrieval
"""

import requests
import json
import time

def test_complete_auth_flow():
    """Test complete authentication flow"""
    base_url = "http://localhost:10000"
    session = requests.Session()
    
    print("🔍 Testing Complete Authentication Flow...")
    
    # Step 1: Test registration
    print("\n1. Testing User Registration...")
    try:
        reg_data = {
            "email": "testuser@example.com",
            "password": "testpass123",
            "api_key": "test_api_key_12345",
            "crn": "test_crn_67890"
        }
        
        response = session.post(f"{base_url}/auth/register", 
                              json=reg_data, 
                              headers={'Content-Type': 'application/json'},
                              timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("   ✅ Registration successful")
            else:
                print(f"   ❌ Registration failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
        return False
    
    # Step 2: Test login
    print("\n2. Testing User Login...")
    try:
        login_data = {
            "email": "testuser@example.com",
            "password": "testpass123"
        }
        
        response = session.post(f"{base_url}/auth/login", 
                              json=login_data, 
                              headers={'Content-Type': 'application/json'},
                              timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("   ✅ Login successful")
                print(f"   🔑 Token received: {result.get('token', '')[:20]}...")
            else:
                print(f"   ❌ Login failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return False
    
    # Step 3: Test dashboard access
    print("\n3. Testing Dashboard Access...")
    try:
        response = session.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Dashboard accessible")
        else:
            print(f"   ❌ Dashboard access failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Dashboard access error: {e}")
        return False
    
    # Step 4: Test protected API endpoints
    print("\n4. Testing Protected API Endpoints...")
    
    endpoints_to_test = [
        "/api/database_stats_secure",
        "/api/job_results",
        "/api/performance_metrics",
        "/api/historical_data",
        "/api/backend_comparison"
    ]
    
    for endpoint in endpoints_to_test:
        try:
            response = session.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ {endpoint}: Success")
                if 'real_data' in result:
                    print(f"      📊 Real data: {result.get('real_data', False)}")
            elif response.status_code == 401:
                print(f"   ❌ {endpoint}: Authentication required")
            else:
                print(f"   ⚠️  {endpoint}: Status {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint}: Error - {e}")
    
    # Step 5: Test logout
    print("\n5. Testing Logout...")
    try:
        response = session.get(f"{base_url}/logout", timeout=10)
        if response.status_code in [200, 302]:
            print("   ✅ Logout successful")
        else:
            print(f"   ⚠️  Logout status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Logout error: {e}")
    
    print("\n✅ Authentication flow testing completed")
    return True

if __name__ == "__main__":
    print("🚀 Starting Authentication Flow Testing...")
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    
    success = test_complete_auth_flow()
    
    if success:
        print("\n🎉 Authentication flow test passed!")
    else:
        print("\n💥 Authentication flow test failed!")
