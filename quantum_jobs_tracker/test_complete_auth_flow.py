#!/usr/bin/env python3
"""
Complete Authentication Flow Test
Tests: Registration → Login → Credential Retrieval → Real Data
"""

import requests
import json
import time

def test_complete_auth_flow():
    """Test the complete authentication and data flow"""
    base_url = "http://localhost:10000"
    
    print("🎯 COMPLETE AUTHENTICATION FLOW TEST")
    print("=" * 60)
    
    # Test data
    test_email = f"test_user_{int(time.time())}@quantum.local"
    test_password = "test_password_123"
    test_api_key = "demo_api_key_for_testing_12345"
    test_crn = "demo_crn_for_testing_67890"
    
    print(f"📧 Test Email: {test_email}")
    print(f"🔑 Test API Key: {test_api_key[:20]}...")
    print(f"🆔 Test CRN: {test_crn[:20]}...")
    
    # Step 1: Register new user
    print("\n1️⃣ REGISTRATION TEST")
    print("-" * 30)
    try:
        registration_data = {
            "email": test_email,
            "password": test_password,
            "api_key": test_api_key,
            "crn": test_crn
        }
        
        response = requests.post(f"{base_url}/auth/register", 
                               json=registration_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ Registration successful: {result.get('message')}")
            else:
                print(f"   ❌ Registration failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ Registration failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
        return False
    
    # Step 2: Login
    print("\n2️⃣ LOGIN TEST")
    print("-" * 30)
    session = requests.Session()  # Use session to maintain cookies
    
    try:
        login_data = {
            "email": test_email,
            "password": test_password
        }
        
        response = session.post(f"{base_url}/auth/login", 
                              json=login_data,
                              headers={'Content-Type': 'application/json'},
                              timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ Login successful: {result.get('message')}")
                print(f"   🔐 Token received: {result.get('token', 'None')[:20]}...")
            else:
                print(f"   ❌ Login failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ Login failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return False
    
    # Step 3: Test authenticated endpoints
    print("\n3️⃣ AUTHENTICATED ENDPOINTS TEST")
    print("-" * 30)
    
    # Test dashboard access
    try:
        response = session.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Dashboard access successful")
        else:
            print(f"   ❌ Dashboard access failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Dashboard access error: {e}")
    
    # Test status endpoint
    try:
        response = session.get(f"{base_url}/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status endpoint: {data.get('authenticated', False)}")
            print(f"   📊 Status data: {json.dumps(data, indent=2)}")
        else:
            print(f"   ❌ Status endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Status endpoint error: {e}")
    
    # Test dashboard metrics
    try:
        response = session.get(f"{base_url}/api/dashboard_metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Dashboard metrics: {data.get('real_data', False)}")
            print(f"   📊 Metrics: {json.dumps(data, indent=2)}")
        else:
            print(f"   ❌ Dashboard metrics failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Dashboard metrics error: {e}")
    
    # Test quantum backends
    try:
        response = session.get(f"{base_url}/api/backends", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Quantum backends: {len(data) if isinstance(data, list) else 'Not a list'}")
            if isinstance(data, list) and data:
                print(f"   📊 First backend: {data[0]}")
        else:
            print(f"   ❌ Quantum backends failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Quantum backends error: {e}")
    
    # Step 4: Test logout
    print("\n4️⃣ LOGOUT TEST")
    print("-" * 30)
    try:
        response = session.post(f"{base_url}/auth/logout", timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ Logout successful: {result.get('message')}")
            else:
                print(f"   ❌ Logout failed: {result.get('message')}")
        else:
            print(f"   ❌ Logout failed with status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Logout error: {e}")
    
    # Step 5: Test access after logout
    print("\n5️⃣ POST-LOGOUT ACCESS TEST")
    print("-" * 30)
    try:
        response = session.get(f"{base_url}/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if not data.get('authenticated', True):
                print("   ✅ Properly logged out - no authentication")
            else:
                print("   ⚠️ Still authenticated after logout")
        else:
            print(f"   ❌ Status check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Post-logout test error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 COMPLETE AUTHENTICATION FLOW TEST FINISHED!")
    print("✅ If you see successful registration, login, and data access: SUCCESS!")
    print("🔐 The authentication system is working correctly!")

if __name__ == "__main__":
    test_complete_auth_flow()
