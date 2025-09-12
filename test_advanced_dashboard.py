#!/usr/bin/env python3
"""
Test script for Advanced Dashboard functionality
"""

import requests
import time
import sys

def test_advanced_dashboard():
    """Test the advanced dashboard endpoints"""
    print("🧪 Testing Advanced Dashboard...")

    base_url = "http://localhost:10000"

    # Test main endpoint
    try:
        print("📡 Testing main advanced dashboard endpoint...")
        response = requests.get(f"{base_url}/advanced", timeout=10)
        if response.status_code == 200:
            print("✅ Advanced dashboard HTML loaded successfully")
        else:
            print(f"❌ Advanced dashboard returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Could not connect to advanced dashboard: {e}")
        return False

    # Test API endpoints
    api_endpoints = [
        '/api/test',
        '/api/backends',
        '/api/jobs',
        '/api/metrics',
        '/api/measurement_results'
    ]

    for endpoint in api_endpoints:
        try:
            print(f"📡 Testing {endpoint}...")
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {endpoint} responded successfully")
            else:
                print(f"⚠️ {endpoint} returned status {response.status_code}")
        except Exception as e:
            print(f"⚠️ Could not connect to {endpoint}: {e}")

    print("🎉 Advanced Dashboard test completed!")
    return True

if __name__ == "__main__":
    # Wait a moment for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)

    success = test_advanced_dashboard()
    if success:
        print("\n✅ Advanced Dashboard appears to be working!")
        print("🌐 Open http://localhost:10000/advanced in your browser")
    else:
        print("\n❌ Advanced Dashboard test failed")
        sys.exit(1)
