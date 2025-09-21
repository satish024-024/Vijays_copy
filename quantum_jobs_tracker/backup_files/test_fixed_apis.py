#!/usr/bin/env python3
"""
Quick test to verify all APIs are fixed and working with real data
"""

import requests
import json

def test_fixed_apis():
    """Test that APIs are now working with real data"""
    base_url = "http://localhost:10000"
    
    print("🚀 TESTING FIXED APIs")
    print("=" * 30)
    
    # Test 1: Dashboard metrics (should now require auth)
    print("\n1. Dashboard Metrics:")
    try:
        response = requests.get(f"{base_url}/api/dashboard_metrics", timeout=10)
        if response.status_code == 401:
            print("   ✅ GOOD: Now requires authentication (no more mock data)")
        elif response.status_code == 200:
            data = response.json()
            if data.get('real_data') == True:
                print("   ✅ EXCELLENT: Real data received!")
            else:
                print("   ⚠️  Still getting mock data")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Backends (should work with credentials)
    print("\n2. Quantum Backends:")
    try:
        response = requests.get(f"{base_url}/api/backends", timeout=15)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                print(f"   ✅ Found {len(data)} backends")
                # Check for real IBM backend names
                real_names = ['ibmq_', 'ibm_']
                has_real = any(any(name in str(backend) for name in real_names) for backend in data)
                if has_real:
                    print("   ✅ REAL IBM backends found!")
                else:
                    print("   ⚠️  No real IBM backend names")
            else:
                print("   📭 No backends data")
        else:
            print(f"   ❌ Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Jobs
    print("\n3. Quantum Jobs:")
    try:
        response = requests.get(f"{base_url}/api/jobs", timeout=15)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                print(f"   ✅ Found {len(data)} jobs")
            else:
                print("   📭 No jobs data")
        else:
            print(f"   ❌ Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 30)
    print("🎯 SUMMARY:")
    print("✅ If you see 'REAL data' messages: APIs are working!")
    print("⚠️  If you see 'requires authentication': Login first")
    print("❌ If you see errors: Check server is running on port 10000")
    print("\n💡 Next steps:")
    print("1. Start server: python real_quantum_app.py")
    print("2. Go to: http://localhost:10000/auth")
    print("3. Login with IBM Quantum credentials")
    print("4. Test APIs again")

if __name__ == "__main__":
    test_fixed_apis()
