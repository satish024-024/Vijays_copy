#!/usr/bin/env python3
"""
Test script to verify dashboard connection fixes
"""

import requests
import json
import time

def test_api_endpoints():
    """Test the API endpoints to ensure they work properly"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Dashboard API Endpoints...")
    print("=" * 50)
    
    # Test backends endpoint
    print("\n1. Testing /api/backends endpoint...")
    try:
        response = requests.get(f"{base_url}/api/backends", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Backends API working - {len(data)} backends returned")
            if data:
                print(f"   📊 Sample backend: {data[0].get('name', 'Unknown')}")
        else:
            print(f"   ❌ Backends API failed - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Backends API error: {e}")
    
    # Test jobs endpoint
    print("\n2. Testing /api/jobs endpoint...")
    try:
        response = requests.get(f"{base_url}/api/jobs", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Jobs API working - {len(data)} jobs returned")
            if data:
                print(f"   📊 Sample job: {data[0].get('job_id', 'Unknown')}")
        else:
            print(f"   ❌ Jobs API failed - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Jobs API error: {e}")
    
    # Test job results endpoint
    print("\n3. Testing /api/job_results endpoint...")
    try:
        response = requests.get(f"{base_url}/api/job_results", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Job Results API working - {len(data)} results returned")
        elif response.status_code == 401:
            print(f"   ⚠️ Job Results API requires authentication - Status: {response.status_code}")
        else:
            print(f"   ❌ Job Results API failed - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Job Results API error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Test Summary:")
    print("   - If all endpoints return data, the connection is working")
    print("   - If some return empty arrays, that's normal for new installations")
    print("   - If you see errors, check the server logs for details")

def test_dashboard_page():
    """Test if the dashboard page loads"""
    base_url = "http://localhost:5000"
    
    print("\n🌐 Testing Dashboard Page...")
    try:
        response = requests.get(f"{base_url}/dashboard", timeout=10)
        if response.status_code == 200:
            print("   ✅ Dashboard page loads successfully")
            if "hackathon_dashboard.js" in response.text:
                print("   ✅ Dashboard JavaScript file is included")
            else:
                print("   ⚠️ Dashboard JavaScript file not found in page")
        else:
            print(f"   ❌ Dashboard page failed - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Dashboard page error: {e}")

if __name__ == "__main__":
    print("🚀 Dashboard Connection Test")
    print("Make sure the Flask server is running on localhost:5000")
    print()
    
    test_api_endpoints()
    test_dashboard_page()
    
    print("\n✅ Test completed!")
    print("If you see any errors above, check the server logs for more details.")
