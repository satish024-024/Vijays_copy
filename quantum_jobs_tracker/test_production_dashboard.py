#!/usr/bin/env python3
"""
Test script for Production Dashboard
Tests the production dashboard functionality and integration
"""

import requests
import json
import time
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_production_dashboard():
    """Test the production dashboard functionality"""
    print("🧪 Testing Production Dashboard...")
    
    base_url = "http://localhost:5000"
    
    # Test 1: Check if production dashboard route exists
    print("\n1. Testing production dashboard route...")
    try:
        response = requests.get(f"{base_url}/production-dashboard", timeout=10)
        if response.status_code == 200:
            print("✅ Production dashboard route accessible")
        elif response.status_code == 302:
            print("⚠️  Production dashboard redirects (likely to login) - this is expected")
        else:
            print(f"❌ Production dashboard returned status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error accessing production dashboard: {e}")
    
    # Test 2: Check if API endpoints are working
    print("\n2. Testing API endpoints...")
    api_endpoints = [
        "/api/backends",
        "/api/jobs", 
        "/api/dashboard_metrics",
        "/api/dashboard_state"
    ]
    
    for endpoint in api_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint} - {len(data) if isinstance(data, list) else 'OK'}")
            else:
                print(f"⚠️  {endpoint} - Status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Error: {e}")
    
    # Test 3: Check if static files are accessible
    print("\n3. Testing static files...")
    static_files = [
        "/static/production_dashboard.js",
        "/static/hackathon_dashboard.js"
    ]
    
    for file_path in static_files:
        try:
            response = requests.get(f"{base_url}{file_path}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {file_path} - {len(response.content)} bytes")
            else:
                print(f"❌ {file_path} - Status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {file_path} - Error: {e}")
    
    print("\n🎯 Production Dashboard Test Complete!")
    print("\nTo access the production dashboard:")
    print("1. Start the server: python real_quantum_app.py")
    print("2. Open browser: http://localhost:5000/production-dashboard")
    print("3. Login with your credentials")
    print("4. Enjoy the new gray-themed production dashboard!")

def test_dashboard_features():
    """Test specific dashboard features"""
    print("\n🔧 Testing Dashboard Features...")
    
    # Test if the HTML file exists and has correct structure
    html_file = "templates/production_dashboard.html"
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for key elements
        checks = [
            ("Quantum Nexus", "Dashboard title"),
            ("ProductionDashboard", "JavaScript class"),
            ("production_dashboard.js", "JavaScript file reference"),
            ("widget-grid", "Widget container"),
            ("metrics-grid", "Metrics container"),
            ("bloch-sphere", "Bloch sphere widget"),
            ("circuit", "Circuit widget"),
            ("ai-assistant", "AI assistant widget")
        ]
        
        for check, description in checks:
            if check in content:
                print(f"✅ {description} found")
            else:
                print(f"❌ {description} missing")
    else:
        print("❌ Production dashboard HTML file not found")

if __name__ == "__main__":
    print("🚀 Production Dashboard Test Suite")
    print("=" * 50)
    
    test_dashboard_features()
    test_production_dashboard()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
