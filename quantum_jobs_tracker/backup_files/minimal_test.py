#!/usr/bin/env python3
"""
Minimal Test
Tests just the basic functionality
"""

import requests
import json
import time

def minimal_test():
    """Minimal test"""
    base_url = "http://localhost:10000"
    session = requests.Session()
    
    print("🚀 Minimal Test...")
    
    # Test 1: Auth page
    print("\n1. Testing auth page...")
    try:
        response = requests.get(f"{base_url}/auth", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Auth page works")
        else:
            print("   ❌ Auth page failed")
    except Exception as e:
        print(f"   ❌ Auth page error: {e}")
    
    # Test 2: Register
    print("\n2. Testing registration...")
    try:
        reg_data = {
            "email": "minimal@test.com",
            "password": "testpass123",
            "api_key": "test_api_key_12345",
            "crn": "test_crn_67890"
        }
        
        response = session.post(f"{base_url}/auth/register", json=reg_data, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Success: {result.get('success', False)}")
            print(f"   Message: {result.get('message', 'No message')}")
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
    
    # Test 3: Login
    print("\n3. Testing login...")
    try:
        login_data = {"email": "minimal@test.com", "password": "testpass123"}
        response = session.post(f"{base_url}/auth/login", json=login_data, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Success: {result.get('success', False)}")
            print(f"   Message: {result.get('message', 'No message')}")
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Login error: {e}")
    
    # Test 4: Try dashboard with shorter timeout
    print("\n4. Testing dashboard (short timeout)...")
    try:
        response = session.get(f"{base_url}/", timeout=3)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Dashboard works")
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Dashboard error: {e}")
    
    print("\n✅ Minimal test completed")

if __name__ == "__main__":
    minimal_test()
