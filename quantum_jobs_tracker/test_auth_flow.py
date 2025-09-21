#!/usr/bin/env python3
"""
Test script to verify authentication flow works correctly
"""

import requests
import json
import time

def test_auth_flow():
    """Test the complete authentication flow"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Quantum Spark Authentication Flow")
    print("=" * 50)
    
    # Test 1: Main route should redirect to auth
    print("\n1. Testing main route redirect...")
    try:
        response = requests.get(f"{base_url}/", allow_redirects=False)
        if response.status_code == 302 and '/auth' in response.headers.get('Location', ''):
            print("✅ Main route correctly redirects to /auth")
        else:
            print(f"❌ Main route redirect failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Main route test failed: {e}")
    
    # Test 2: Modern dashboard should redirect to auth when not authenticated
    print("\n2. Testing modern dashboard without authentication...")
    try:
        response = requests.get(f"{base_url}/modern_dashboard", allow_redirects=False)
        if response.status_code == 302 and '/auth' in response.headers.get('Location', ''):
            print("✅ Modern dashboard correctly redirects to /auth when not authenticated")
        else:
            print(f"❌ Modern dashboard redirect failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Modern dashboard test failed: {e}")
    
    # Test 3: Auth page should be accessible
    print("\n3. Testing auth page accessibility...")
    try:
        response = requests.get(f"{base_url}/auth")
        if response.status_code == 200:
            print("✅ Auth page is accessible")
        else:
            print(f"❌ Auth page not accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Auth page test failed: {e}")
    
    # Test 4: Test user registration
    print("\n4. Testing user registration...")
    try:
        test_user = {
            "email": "test@quantum.local",
            "password": "testpassword123",
            "quantum_token": "test_token_123",
            "quantum_crn": "test_crn_123"
        }
        
        response = requests.post(f"{base_url}/auth/register", 
                               json=test_user,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ User registration successful")
            else:
                print(f"⚠️ User registration returned success=False: {data.get('message')}")
        else:
            print(f"❌ User registration failed: {response.status_code}")
    except Exception as e:
        print(f"❌ User registration test failed: {e}")
    
    # Test 5: Test user login
    print("\n5. Testing user login...")
    try:
        login_data = {
            "email": "test@quantum.local",
            "password": "testpassword123"
        }
        
        response = requests.post(f"{base_url}/auth/login", 
                               json=login_data,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('redirect') == '/modern_dashboard':
                print("✅ User login successful and redirects to modern dashboard")
                
                # Test 6: Test authenticated access to modern dashboard
                print("\n6. Testing authenticated access to modern dashboard...")
                session = requests.Session()
                
                # First login to get session
                login_response = session.post(f"{base_url}/auth/login", 
                                            json=login_data,
                                            headers={'Content-Type': 'application/json'})
                
                if login_response.status_code == 200:
                    # Now try to access modern dashboard with session
                    dashboard_response = session.get(f"{base_url}/modern_dashboard")
                    if dashboard_response.status_code == 200:
                        print("✅ Authenticated access to modern dashboard successful")
                    else:
                        print(f"❌ Authenticated access to modern dashboard failed: {dashboard_response.status_code}")
                else:
                    print("❌ Could not establish session for dashboard test")
            else:
                print(f"❌ Login failed or wrong redirect: {data}")
        else:
            print(f"❌ User login failed: {response.status_code}")
    except Exception as e:
        print(f"❌ User login test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Authentication Flow Test Complete")
    print("=" * 50)

if __name__ == "__main__":
    test_auth_flow()
