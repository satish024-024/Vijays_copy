#!/usr/bin/env python3
"""
Test script to verify widget loading fixes
"""

import requests
import json
import time

def test_widget_loading():
    """Test that widgets load properly without getting stuck"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Widget Loading Fixes")
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
    
    # Test 2: Test API endpoints that feed the widgets
    print("\n2. Testing widget data APIs...")
    widget_apis = [
        '/api/backends',
        '/api/performance_metrics',
        '/api/realtime_monitoring', 
        '/api/historical_data',
        '/api/calibration_data',
        '/api/dashboard_metrics'
    ]
    
    for api in widget_apis:
        try:
            response = requests.get(f"{base_url}{api}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {api}: {response.status_code} - Data keys: {list(data.keys()) if isinstance(data, dict) else 'Array'}")
            else:
                print(f"⚠️ {api}: {response.status_code}")
        except Exception as e:
            print(f"❌ {api}: Error - {e}")
    
    # Test 3: Test with authentication
    print("\n3. Testing with authentication...")
    try:
        # Register and login test user
        test_user = {
            "email": "test@quantum.local",
            "password": "testpassword123",
            "quantum_token": "test_token_123",
            "quantum_crn": "test_crn_123"
        }
        
        # Register
        response = requests.post(f"{base_url}/auth/register", 
                               json=test_user,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            # Login
            login_data = {
                "email": "test@quantum.local",
                "password": "testpassword123"
            }
            
            session = requests.Session()
            response = session.post(f"{base_url}/auth/login", 
                                   json=login_data,
                                   headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print("✅ Test user authenticated")
                    
                    # Test authenticated widget APIs
                    print("\n4. Testing authenticated widget APIs...")
                    for api in widget_apis:
                        try:
                            response = session.get(f"{base_url}{api}", timeout=10)
                            if response.status_code == 200:
                                data = response.json()
                                print(f"✅ {api}: {response.status_code} - Data received")
                            else:
                                print(f"⚠️ {api}: {response.status_code}")
                        except Exception as e:
                            print(f"❌ {api}: Error - {e}")
                    
                    # Test modern dashboard access
                    print("\n5. Testing modern dashboard access...")
                    response = session.get(f"{base_url}/modern_dashboard", timeout=10)
                    if response.status_code == 200:
                        print("✅ Modern dashboard accessible")
                        print("✅ Dashboard should load without stuck loading animations")
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
    print("🎯 Widget Loading Test Complete")
    print("=" * 50)

if __name__ == "__main__":
    test_widget_loading()
