#!/usr/bin/env python3
"""
Test script to verify dashboard fixes work correctly
"""

import requests
import json
import time

def test_dashboard_fixes():
    """Test that all dashboard fixes are working"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Dashboard Fixes")
    print("=" * 50)
    
    # Test 1: Check if application is running
    print("\n1. Testing application status...")
    try:
        response = requests.get(f"{base_url}/test", timeout=5)
        if response.status_code == 200:
            print("✅ Application is running")
        else:
            print(f"❌ Application not responding: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to application: {e}")
        return
    
    # Test 2: Check authentication redirect
    print("\n2. Testing authentication redirect...")
    try:
        response = requests.get(f"{base_url}/modern_dashboard", allow_redirects=False)
        if response.status_code == 302 and '/auth' in response.headers.get('Location', ''):
            print("✅ Modern dashboard correctly redirects to auth when not authenticated")
        else:
            print(f"❌ Modern dashboard redirect failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Authentication redirect test failed: {e}")
    
    # Test 3: Check API endpoints without authentication
    print("\n3. Testing API endpoints without authentication...")
    endpoints = [
        '/api/backends',
        '/api/performance_metrics', 
        '/api/realtime_monitoring',
        '/api/historical_data',
        '/api/calibration_data'
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code in [200, 401]:  # 200 for working, 401 for auth required
                print(f"✅ {endpoint}: {response.status_code}")
            else:
                print(f"⚠️ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")
    
    # Test 4: Test with authentication (simulate login)
    print("\n4. Testing with authentication...")
    try:
        # First register a test user
        test_user = {
            "email": "test@quantum.local",
            "password": "testpassword123",
            "quantum_token": "test_token_123",
            "quantum_crn": "test_crn_123"
        }
        
        # Register user
        response = requests.post(f"{base_url}/auth/register", 
                               json=test_user,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            print("✅ Test user registered")
            
            # Login user
            login_data = {
                "email": "test@quantum.local",
                "password": "testpassword123"
            }
            
            response = requests.post(f"{base_url}/auth/login", 
                                   json=login_data,
                                   headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print("✅ Test user logged in")
                    
                    # Create session for authenticated requests
                    session = requests.Session()
                    session.post(f"{base_url}/auth/login", 
                               json=login_data,
                               headers={'Content-Type': 'application/json'})
                    
                    # Test authenticated endpoints
                    print("\n5. Testing authenticated API endpoints...")
                    for endpoint in endpoints:
                        try:
                            response = session.get(f"{base_url}{endpoint}", timeout=5)
                            if response.status_code == 200:
                                print(f"✅ {endpoint}: {response.status_code} (authenticated)")
                            else:
                                print(f"⚠️ {endpoint}: {response.status_code} (authenticated)")
                        except Exception as e:
                            print(f"❌ {endpoint}: Error - {e}")
                    
                    # Test modern dashboard access
                    print("\n6. Testing modern dashboard access...")
                    response = session.get(f"{base_url}/modern_dashboard", timeout=5)
                    if response.status_code == 200:
                        print("✅ Modern dashboard accessible with authentication")
                    else:
                        print(f"❌ Modern dashboard access failed: {response.status_code}")
                        
                else:
                    print(f"❌ Login failed: {data.get('message')}")
            else:
                print(f"❌ Login request failed: {response.status_code}")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Dashboard Fixes Test Complete")
    print("=" * 50)

if __name__ == "__main__":
    test_dashboard_fixes()
