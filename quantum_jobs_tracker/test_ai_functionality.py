#!/usr/bin/env python3
"""
Test script to verify AI functionality is working correctly
"""
import requests
import json
import time

def test_ai_functionality():
    base_url = "http://localhost:10000"
    
    print("🧪 Testing AI Functionality...")
    print("=" * 50)
    
    # Test 1: Check if server is running
    print("1. Testing server connectivity...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   ✅ Server is running (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Server not accessible: {e}")
        return False
    
    # Test 2: Test AI circuit generation (should work without auth)
    print("\n2. Testing AI circuit generation...")
    try:
        response = requests.post(
            f"{base_url}/api/ai-generate-circuit",
            json={"query": "Create a Bell state circuit"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Circuit generation works: {data.get('circuit', {}).get('name', 'Unknown')}")
        else:
            print(f"   ❌ Circuit generation failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Circuit generation error: {e}")
    
    # Test 3: Test AI circuit submission (should work in demo mode)
    print("\n3. Testing AI circuit submission...")
    try:
        response = requests.post(
            f"{base_url}/api/ai-submit-circuit",
            json={
                "type": "bell_state",
                "params": {"qubits": 2, "shots": 1024},
                "backend": "ibm_brisbane"
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ Circuit submission works: {data.get('message', 'Success')}")
                if data.get('demo_mode'):
                    print(f"   🎭 Demo mode active: {data.get('job_id', 'Unknown ID')}")
            else:
                print(f"   ❌ Circuit submission failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"   ❌ Circuit submission failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Circuit submission error: {e}")
    
    # Test 4: Test 3D circuit generation
    print("\n4. Testing 3D circuit generation...")
    try:
        response = requests.post(
            f"{base_url}/api/ai-circuit-3d",
            json={
                "type": "bell_state",
                "params": {"qubits": 2, "shots": 1024}
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ 3D circuit generation works: {data.get('circuit_3d', {}).get('name', 'Unknown')}")
            else:
                print(f"   ❌ 3D circuit generation failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"   ❌ 3D circuit generation failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ 3D circuit generation error: {e}")
    
    # Test 5: Test dashboard endpoints
    print("\n5. Testing dashboard endpoints...")
    endpoints = [
        "/api/backends",
        "/api/jobs", 
        "/api/dashboard_metrics"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {endpoint} works")
            else:
                print(f"   ⚠️  {endpoint} returned {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint} error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 AI Functionality Test Complete!")
    print("If you see errors above, the AI system needs fixes.")
    print("If all tests pass, the AI system is working correctly.")

if __name__ == "__main__":
    test_ai_functionality()
