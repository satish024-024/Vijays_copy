#!/usr/bin/env python3
"""
Final test to verify authentication and data retrieval works
"""

import requests
import json
import time

def test_final_fix():
    """Test the complete authentication and data flow"""
    base_url = "http://localhost:10000"
    
    print("🎯 FINAL TEST - Authentication & Real Data Flow")
    print("=" * 50)
    
    # Test 1: Set credentials
    print("\n1. Setting IBM Quantum credentials...")
    try:
        # Use demo credentials for testing
        credentials = {
            "token": "demo_token_for_testing_12345",
            "crn": "demo_crn_for_testing_67890"
        }
        
        response = requests.post(f"{base_url}/token", 
                               json=credentials,
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Credentials set: {result.get('message', 'Success')}")
        else:
            print(f"   ❌ Failed to set credentials: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error setting credentials: {e}")
        return False
    
    # Wait a moment for background connection
    print("\n2. Waiting for background connection...")
    time.sleep(3)
    
    # Test 2: Check authentication status
    print("\n3. Checking authentication status...")
    try:
        response = requests.get(f"{base_url}/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data.get('authenticated', False)}")
            print(f"   📊 Data: {json.dumps(data, indent=2)}")
        else:
            print(f"   ❌ Status failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Status error: {e}")
    
    # Test 3: Check dashboard metrics
    print("\n4. Checking dashboard metrics...")
    try:
        response = requests.get(f"{base_url}/api/dashboard_metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Metrics received")
            print(f"   📊 Data: {json.dumps(data, indent=2)}")
        elif response.status_code == 401:
            print(f"   🔐 Requires authentication (expected)")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Metrics error: {e}")
    
    # Test 4: Check backends
    print("\n5. Checking quantum backends...")
    try:
        response = requests.get(f"{base_url}/api/backends", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Backends received: {len(data) if isinstance(data, list) else 'Not a list'}")
            if isinstance(data, list) and data:
                print(f"   📊 First backend: {data[0]}")
        else:
            print(f"   ❌ Backends failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Backends error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 TEST COMPLETED!")
    print("✅ If you see credentials set and data received: SUCCESS!")
    print("⚠️  If you see authentication required: Login first in browser")

if __name__ == "__main__":
    test_final_fix()
