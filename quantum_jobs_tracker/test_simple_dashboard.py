#!/usr/bin/env python3
"""
Test Simple Dashboard
Tests the simplified dashboard route
"""

import requests
import json
import time

def test_simple_dashboard():
    """Test simple dashboard"""
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    print("🚀 Testing Simple Dashboard...")
    
    # Login first
    print("\n1. Logging in...")
    try:
        login_data = {"email": "minimal@test.com", "password": "testpass123"}
        response = session.post(f"{base_url}/auth/login", json=login_data, timeout=5)
        if response.status_code == 200:
            print("   ✅ Login successful")
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return False
    
    # Test simple dashboard
    print("\n2. Testing simple dashboard...")
    try:
        response = session.get(f"{base_url}/test-dashboard", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Simple dashboard works!")
            print(f"   Content length: {len(response.text)}")
        else:
            print(f"   ❌ Simple dashboard failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Simple dashboard error: {e}")
    
    # Test main dashboard
    print("\n3. Testing main dashboard...")
    try:
        response = session.get(f"{base_url}/", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Main dashboard works!")
        else:
            print(f"   ❌ Main dashboard failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Main dashboard error: {e}")
    
    print("\n✅ Simple dashboard test completed")

if __name__ == "__main__":
    test_simple_dashboard()
