#!/usr/bin/env python3
"""
Quick System Test
Tests the system quickly to verify everything is working
"""

import requests
import json
import time

def quick_test():
    """Quick test of the system"""
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    print("🚀 Quick System Test...")
    
    # Test 1: Check if server is running
    print("\n1. Checking server status...")
    try:
        response = requests.get(f"{base_url}/auth", timeout=5)
        if response.status_code == 200:
            print("   ✅ Server is running")
        else:
            print(f"   ❌ Server error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Server not accessible: {e}")
        return False
    
    # Test 2: Test registration and login
    print("\n2. Testing authentication...")
    try:
        # Register
        reg_data = {
            "email": "quicktest@example.com",
            "password": "testpass123",
            "api_key": "test_api_key_12345",
            "crn": "test_crn_67890"
        }
        
        response = session.post(f"{base_url}/auth/register", json=reg_data, timeout=5)
        if response.status_code != 200:
            print(f"   ❌ Registration failed: {response.status_code}")
            return False
        
        # Login
        login_data = {"email": "quicktest@example.com", "password": "testpass123"}
        response = session.post(f"{base_url}/auth/login", json=login_data, timeout=5)
        if response.status_code != 200:
            print(f"   ❌ Login failed: {response.status_code}")
            return False
        
        print("   ✅ Authentication working")
    except Exception as e:
        print(f"   ❌ Authentication error: {e}")
        return False
    
    # Test 3: Test dashboard access
    print("\n3. Testing dashboard access...")
    try:
        response = session.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Dashboard accessible")
        else:
            print(f"   ❌ Dashboard error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Dashboard error: {e}")
        return False
    
    # Test 4: Test API endpoints
    print("\n4. Testing API endpoints...")
    endpoints = [
        "/api/database_stats_secure",
        "/api/job_results",
        "/api/performance_metrics"
    ]
    
    for endpoint in endpoints:
        try:
            response = session.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ {endpoint}: Success")
                if 'real_data' in result:
                    print(f"      📊 Real data: {result.get('real_data', False)}")
            else:
                print(f"   ❌ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint}: {e}")
    
    print("\n✅ Quick test completed successfully!")
    return True

if __name__ == "__main__":
    success = quick_test()
    if success:
        print("\n🎉 System is working correctly!")
    else:
        print("\n💥 System has issues!")
