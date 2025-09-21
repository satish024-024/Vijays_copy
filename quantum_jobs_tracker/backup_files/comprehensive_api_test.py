#!/usr/bin/env python3
"""
Comprehensive API Testing Script
Tests all API endpoints, data retrieval, and IBM Quantum connectivity
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
import threading
import subprocess

class APITester:
    def __init__(self, base_url="http://localhost:10000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        self.test_results = {}
        
    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_emoji = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
        print(f"[{timestamp}] {status_emoji.get(status, 'ℹ️')} {message}")
        
    def test_server_running(self):
        """Test if the server is running"""
        self.log("Testing if server is running...")
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            if response.status_code in [200, 302, 401]:
                self.log("Server is running and responding", "SUCCESS")
                return True
            else:
                self.log(f"Server responded with status {response.status_code}", "WARNING")
                return True
        except requests.exceptions.ConnectionError:
            self.log("Server is not running or not accessible", "ERROR")
            self.log("Please start the server first with: python real_quantum_app.py", "ERROR")
            return False
        except Exception as e:
            self.log(f"Server test failed: {e}", "ERROR")
            return False
    
    def test_authentication_flow(self):
        """Test user registration and login"""
        self.log("Testing authentication flow...")
        
        # Generate unique test user
        timestamp = str(int(time.time()))
        test_email = f"test_user_{timestamp}@example.com"
        test_password = "TestPass123!"
        test_api_key = "demo_ibm_token_for_testing"
        test_crn = "demo_crn_for_testing"
        
        # Test 1: Registration
        self.log("Testing user registration...")
        try:
            reg_data = {
                "email": test_email,
                "password": test_password,
                "api_key": test_api_key,
                "crn": test_crn
            }
            response = self.session.post(f"{self.base_url}/auth/register", 
                                       json=reg_data, 
                                       headers={'Content-Type': 'application/json'},
                                       timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.log("User registration successful", "SUCCESS")
                else:
                    self.log(f"Registration failed: {result.get('message')}", "WARNING")
            else:
                self.log(f"Registration endpoint returned {response.status_code}", "WARNING")
        except Exception as e:
            self.log(f"Registration test failed: {e}", "ERROR")
        
        # Test 2: Login
        self.log("Testing user login...")
        try:
            login_data = {
                "email": test_email,
                "password": test_password
            }
            response = self.session.post(f"{self.base_url}/auth/login", 
                                       json=login_data, 
                                       headers={'Content-Type': 'application/json'},
                                       timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.auth_token = result.get('token')
                    self.log("User login successful", "SUCCESS")
                    # Store auth token in session headers
                    self.session.headers.update({'Authorization': f'Bearer {self.auth_token}'})
                    return True
                else:
                    self.log(f"Login failed: {result.get('message')}", "ERROR")
            else:
                self.log(f"Login endpoint returned {response.status_code}", "ERROR")
        except Exception as e:
            self.log(f"Login test failed: {e}", "ERROR")
        
        return False
    
    def test_public_endpoints(self):
        """Test public endpoints that don't require authentication"""
        self.log("Testing public endpoints...")
        
        public_endpoints = [
            ("/", "Dashboard"),
            ("/auth", "Authentication page"),
            ("/status", "Status endpoint"),
            ("/connection_status", "Connection status"),
            ("/api/backends", "Backends list"),
            ("/api/offline_data", "Offline data"),
            ("/api/sync_status", "Sync status")
        ]
        
        for endpoint, description in public_endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    self.log(f"{description} ({endpoint}): Working", "SUCCESS")
                    self.test_results[endpoint] = {"status": "success", "data_received": True}
                elif response.status_code in [401, 403]:
                    self.log(f"{description} ({endpoint}): Requires authentication", "WARNING")
                    self.test_results[endpoint] = {"status": "auth_required", "data_received": False}
                else:
                    self.log(f"{description} ({endpoint}): Status {response.status_code}", "WARNING")
                    self.test_results[endpoint] = {"status": f"status_{response.status_code}", "data_received": False}
            except Exception as e:
                self.log(f"{description} ({endpoint}): Error - {e}", "ERROR")
                self.test_results[endpoint] = {"status": "error", "data_received": False}
    
    def test_data_endpoints(self):
        """Test data retrieval endpoints"""
        self.log("Testing data retrieval endpoints...")
        
        data_endpoints = [
            ("/api/jobs", "Quantum jobs"),
            ("/api/job_results", "Job results"),
            ("/api/performance_metrics", "Performance metrics"),
            ("/api/realtime_monitoring", "Real-time monitoring"),
            ("/api/historical_data", "Historical data"),
            ("/api/calibration_data", "Calibration data"),
            ("/api/dashboard_metrics", "Dashboard metrics"),
            ("/api/quantum_state_data", "Quantum state data"),
            ("/api/circuit_data", "Circuit data"),
            ("/api/database_stats", "Database statistics"),
            ("/api/metrics_history", "Metrics history"),
            ("/api/cached_data/jobs", "Cached jobs data"),
            ("/api/cached_data/backends", "Cached backends data")
        ]
        
        for endpoint, description in data_endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=15)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, dict) and data:
                            self.log(f"{description} ({endpoint}): Data received ({len(str(data))} chars)", "SUCCESS")
                            self.test_results[endpoint] = {"status": "success", "data_received": True, "data_size": len(str(data))}
                        elif isinstance(data, list) and data:
                            self.log(f"{description} ({endpoint}): {len(data)} items received", "SUCCESS")
                            self.test_results[endpoint] = {"status": "success", "data_received": True, "items_count": len(data)}
                        else:
                            self.log(f"{description} ({endpoint}): Empty response", "WARNING")
                            self.test_results[endpoint] = {"status": "empty", "data_received": False}
                    except json.JSONDecodeError:
                        self.log(f"{description} ({endpoint}): Non-JSON response", "WARNING")
                        self.test_results[endpoint] = {"status": "non_json", "data_received": False}
                elif response.status_code in [401, 403]:
                    self.log(f"{description} ({endpoint}): Requires authentication", "WARNING")
                    self.test_results[endpoint] = {"status": "auth_required", "data_received": False}
                else:
                    self.log(f"{description} ({endpoint}): Status {response.status_code}", "WARNING")
                    self.test_results[endpoint] = {"status": f"status_{response.status_code}", "data_received": False}
            except Exception as e:
                self.log(f"{description} ({endpoint}): Error - {e}", "ERROR")
                self.test_results[endpoint] = {"status": "error", "data_received": False}
    
    def test_quantum_connectivity(self):
        """Test IBM Quantum connectivity"""
        self.log("Testing IBM Quantum connectivity...")
        
        try:
            # Test backends endpoint which should show available quantum backends
            response = self.session.get(f"{self.base_url}/api/backends", timeout=20)
            
            if response.status_code == 200:
                try:
                    backends_data = response.json()
                    if isinstance(backends_data, list) and backends_data:
                        self.log(f"Found {len(backends_data)} quantum backends", "SUCCESS")
                        for backend in backends_data[:3]:  # Show first 3
                            if isinstance(backend, dict):
                                name = backend.get('name', 'Unknown')
                                status = backend.get('status', 'Unknown')
                                self.log(f"  - {name}: {status}")
                        self.test_results["quantum_connectivity"] = {"status": "success", "backends_count": len(backends_data)}
                    else:
                        self.log("No quantum backends found (offline mode or no credentials)", "WARNING")
                        self.test_results["quantum_connectivity"] = {"status": "no_backends", "backends_count": 0}
                except json.JSONDecodeError:
                    self.log("Backends endpoint returned non-JSON response", "WARNING")
                    self.test_results["quantum_connectivity"] = {"status": "non_json", "backends_count": 0}
            else:
                self.log(f"Backends endpoint returned status {response.status_code}", "WARNING")
                self.test_results["quantum_connectivity"] = {"status": f"status_{response.status_code}", "backends_count": 0}
                
        except Exception as e:
            self.log(f"Quantum connectivity test failed: {e}", "ERROR")
            self.test_results["quantum_connectivity"] = {"status": "error", "backends_count": 0}
    
    def test_dashboard_functionality(self):
        """Test dashboard-specific functionality"""
        self.log("Testing dashboard functionality...")
        
        dashboard_endpoints = [
            ("/dashboard", "Main dashboard"),
            ("/production-dashboard", "Production dashboard"),
            ("/advanced", "Advanced dashboard"),
            ("/modern", "Modern dashboard"),
            ("/professional", "Professional dashboard"),
            ("/hackathon", "Hackathon dashboard")
        ]
        
        for endpoint, description in dashboard_endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    self.log(f"{description} ({endpoint}): Accessible", "SUCCESS")
                elif response.status_code in [302, 401]:
                    self.log(f"{description} ({endpoint}): Redirected (auth required)", "WARNING")
                else:
                    self.log(f"{description} ({endpoint}): Status {response.status_code}", "WARNING")
            except Exception as e:
                self.log(f"{description} ({endpoint}): Error - {e}", "ERROR")
    
    def test_post_endpoints(self):
        """Test POST endpoints"""
        self.log("Testing POST endpoints...")
        
        # Test quantum gate application
        try:
            gate_data = {
                "gate_type": "h",
                "qubit": 0,
                "circuit_id": "test_circuit"
            }
            response = self.session.post(f"{self.base_url}/api/apply_quantum_gate", 
                                       json=gate_data,
                                       headers={'Content-Type': 'application/json'},
                                       timeout=10)
            
            if response.status_code == 200:
                self.log("Quantum gate application endpoint: Working", "SUCCESS")
            else:
                self.log(f"Quantum gate endpoint: Status {response.status_code}", "WARNING")
        except Exception as e:
            self.log(f"Quantum gate endpoint test failed: {e}", "ERROR")
        
        # Test sync start
        try:
            response = self.session.post(f"{self.base_url}/api/start_sync", 
                                       json={},
                                       headers={'Content-Type': 'application/json'},
                                       timeout=10)
            
            if response.status_code == 200:
                self.log("Sync start endpoint: Working", "SUCCESS")
            else:
                self.log(f"Sync start endpoint: Status {response.status_code}", "WARNING")
        except Exception as e:
            self.log(f"Sync start endpoint test failed: {e}", "ERROR")
    
    def generate_report(self):
        """Generate a comprehensive test report"""
        self.log("Generating test report...")
        
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results.values() if r.get("status") == "success"])
        data_received_tests = len([r for r in self.test_results.values() if r.get("data_received")])
        
        print("\n" + "="*60)
        print("🔍 COMPREHENSIVE API TEST REPORT")
        print("="*60)
        print(f"📊 Total endpoints tested: {total_tests}")
        print(f"✅ Successful responses: {successful_tests}")
        print(f"📡 Endpoints returning data: {data_received_tests}")
        print(f"📈 Success rate: {(successful_tests/total_tests*100):.1f}%" if total_tests > 0 else "📈 Success rate: 0%")
        
        print("\n📋 DETAILED RESULTS:")
        print("-" * 60)
        
        for endpoint, result in self.test_results.items():
            status = result.get("status", "unknown")
            data_received = result.get("data_received", False)
            
            status_emoji = {
                "success": "✅",
                "auth_required": "🔐",
                "empty": "📭",
                "error": "❌",
                "non_json": "⚠️"
            }.get(status, "❓")
            
            data_emoji = "📡" if data_received else "📭"
            
            print(f"{status_emoji} {data_emoji} {endpoint}")
            
            if result.get("items_count"):
                print(f"    └── {result['items_count']} items")
            elif result.get("data_size"):
                print(f"    └── {result['data_size']} characters")
            elif result.get("backends_count") is not None:
                print(f"    └── {result['backends_count']} backends")
        
        print("\n🎯 SUMMARY:")
        print("-" * 60)
        if successful_tests > total_tests * 0.8:
            print("🎉 Excellent! Most endpoints are working properly.")
        elif successful_tests > total_tests * 0.5:
            print("👍 Good! Most endpoints are functional.")
        else:
            print("⚠️  Some issues detected. Check the detailed results above.")
        
        if data_received_tests > 0:
            print(f"📡 Data is being retrieved from {data_received_tests} endpoints.")
        else:
            print("📭 No data received from any endpoints. Check authentication or data sources.")
        
        print("\n💡 RECOMMENDATIONS:")
        print("-" * 60)
        if not self.auth_token:
            print("🔐 Authentication: Register and login to test protected endpoints")
        if self.test_results.get("quantum_connectivity", {}).get("backends_count", 0) == 0:
            print("🌐 Quantum Connectivity: Add valid IBM Quantum credentials for real data")
        print("🚀 Server: Keep the server running for continuous testing")
        print("📊 Monitoring: Use this script regularly to monitor API health")
        
        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "data_received_tests": data_received_tests,
            "success_rate": (successful_tests/total_tests*100) if total_tests > 0 else 0
        }

def main():
    print("🚀 COMPREHENSIVE API TESTING SUITE")
    print("=" * 50)
    print("This script will test all API endpoints and data retrieval")
    print("Make sure your server is running: python real_quantum_app.py")
    print("=" * 50)
    
    # Wait a moment for user to see the message
    time.sleep(2)
    
    tester = APITester()
    
    # Step 1: Check if server is running
    if not tester.test_server_running():
        print("\n❌ Server is not running!")
        print("Please start the server first with:")
        print("   python real_quantum_app.py")
        print("   or")
        print("   python hackathon_dashboard_app.py")
        return False
    
    # Step 2: Test authentication flow
    tester.test_authentication_flow()
    
    # Step 3: Test public endpoints
    tester.test_public_endpoints()
    
    # Step 4: Test data endpoints
    tester.test_data_endpoints()
    
    # Step 5: Test quantum connectivity
    tester.test_quantum_connectivity()
    
    # Step 6: Test dashboard functionality
    tester.test_dashboard_functionality()
    
    # Step 7: Test POST endpoints
    tester.test_post_endpoints()
    
    # Step 8: Generate report
    report = tester.generate_report()
    
    print("\n🏁 Testing completed!")
    
    return report["success_rate"] > 50

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        sys.exit(1)

