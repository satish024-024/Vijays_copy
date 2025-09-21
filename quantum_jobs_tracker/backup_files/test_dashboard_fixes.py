#!/usr/bin/env python3
"""
Test script to verify all dashboard fixes work properly
This script tests the API endpoints and dashboard functionality
"""

import requests
import json
import time
import sys
from datetime import datetime

class DashboardTester:
    def __init__(self, base_url="http://localhost:10000"):
        self.base_url = base_url
        self.test_results = []
        
    def log_test(self, test_name, success, message="", details=None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details:
            print(f"   Details: {details}")
    
    def test_api_endpoint(self, endpoint, expected_keys=None):
        """Test an API endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if response has expected structure
                if expected_keys:
                    missing_keys = [key for key in expected_keys if key not in data]
                    if missing_keys:
                        self.log_test(f"API {endpoint}", False, f"Missing keys: {missing_keys}")
                        return False
                
                self.log_test(f"API {endpoint}", True, f"Status: {response.status_code}, Data keys: {list(data.keys())}")
                return True
            else:
                self.log_test(f"API {endpoint}", False, f"HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test(f"API {endpoint}", False, f"Request failed: {str(e)}")
            return False
        except json.JSONDecodeError as e:
            self.log_test(f"API {endpoint}", False, f"Invalid JSON: {str(e)}")
            return False
    
    def test_backends_api(self):
        """Test the backends API endpoint"""
        print("\n🔍 Testing Backends API...")
        
        try:
            url = f"{self.base_url}/api/backends"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check new API structure
                required_keys = ['backends', 'connection_status', 'total_backends', 'active_backends', 'real_data', 'status']
                missing_keys = [key for key in required_keys if key not in data]
                
                if missing_keys:
                    self.log_test("Backends API Structure", False, f"Missing keys: {missing_keys}")
                else:
                    self.log_test("Backends API Structure", True, "All required keys present")
                
                # Check backends data
                if 'backends' in data and isinstance(data['backends'], list):
                    backends = data['backends']
                    self.log_test("Backends Data", True, f"Found {len(backends)} backends")
                    
                    # Check backend structure
                    if backends:
                        backend = backends[0]
                        backend_keys = ['name', 'status', 'num_qubits', 'pending_jobs', 'operational', 'tier', 'real_data']
                        missing_backend_keys = [key for key in backend_keys if key not in backend]
                        
                        if missing_backend_keys:
                            self.log_test("Backend Structure", False, f"Missing backend keys: {missing_backend_keys}")
                        else:
                            self.log_test("Backend Structure", True, "Backend structure is correct")
                else:
                    self.log_test("Backends Data", False, "No backends array found")
                
                return True
            else:
                self.log_test("Backends API", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Backends API", False, f"Error: {str(e)}")
            return False
    
    def test_jobs_api(self):
        """Test the jobs API endpoint"""
        print("\n🔍 Testing Jobs API...")
        
        try:
            url = f"{self.base_url}/api/jobs"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check new API structure
                required_keys = ['jobs', 'connection_status', 'total_jobs', 'running_jobs', 'completed_jobs', 'real_data', 'status']
                missing_keys = [key for key in required_keys if key not in data]
                
                if missing_keys:
                    self.log_test("Jobs API Structure", False, f"Missing keys: {missing_keys}")
                else:
                    self.log_test("Jobs API Structure", True, "All required keys present")
                
                # Check jobs data
                if 'jobs' in data and isinstance(data['jobs'], list):
                    jobs = data['jobs']
                    self.log_test("Jobs Data", True, f"Found {len(jobs)} jobs")
                    
                    # Check job structure
                    if jobs:
                        job = jobs[0]
                        job_keys = ['job_id', 'id', 'backend', 'status', 'created_at', 'real_data']
                        missing_job_keys = [key for key in job_keys if key not in job]
                        
                        if missing_job_keys:
                            self.log_test("Job Structure", False, f"Missing job keys: {missing_job_keys}")
                        else:
                            self.log_test("Job Structure", True, "Job structure is correct")
                else:
                    self.log_test("Jobs Data", False, "No jobs array found")
                
                return True
            else:
                self.log_test("Jobs API", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Jobs API", False, f"Error: {str(e)}")
            return False
    
    def test_dashboard_state_api(self):
        """Test the dashboard state API endpoint"""
        print("\n🔍 Testing Dashboard State API...")
        
        try:
            url = f"{self.base_url}/api/dashboard_state"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required keys
                required_keys = ['active_backends', 'total_jobs', 'running_jobs', 'connection_status', 'real_data', 'status']
                missing_keys = [key for key in required_keys if key not in data]
                
                if missing_keys:
                    self.log_test("Dashboard State Structure", False, f"Missing keys: {missing_keys}")
                else:
                    self.log_test("Dashboard State Structure", True, "All required keys present")
                
                # Check connection status structure
                if 'connection_status' in data:
                    conn_status = data['connection_status']
                    if isinstance(conn_status, dict):
                        if 'is_connected' in conn_status and 'status' in conn_status:
                            self.log_test("Connection Status Structure", True, "Connection status structure is correct")
                        else:
                            self.log_test("Connection Status Structure", False, "Missing is_connected or status")
                    else:
                        self.log_test("Connection Status Structure", False, "Connection status should be an object")
                
                return True
            else:
                self.log_test("Dashboard State API", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Dashboard State API", False, f"Error: {str(e)}")
            return False
    
    def test_dashboard_page(self):
        """Test if the dashboard page loads"""
        print("\n🔍 Testing Dashboard Page...")
        
        try:
            url = f"{self.base_url}/"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                
                # Check if dashboard_fixed.js is referenced
                if 'dashboard_fixed.js' in content:
                    self.log_test("Dashboard Page", True, "dashboard_fixed.js is referenced")
                else:
                    self.log_test("Dashboard Page", False, "dashboard_fixed.js not found in page")
                
                # Check if required elements exist
                required_elements = ['connection-status', 'active-backends', 'total-jobs', 'running-jobs']
                missing_elements = [elem for elem in required_elements if f'id="{elem}"' not in content]
                
                if missing_elements:
                    self.log_test("Dashboard Elements", False, f"Missing elements: {missing_elements}")
                else:
                    self.log_test("Dashboard Elements", True, "All required elements present")
                
                return True
            else:
                self.log_test("Dashboard Page", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Dashboard Page", False, f"Error: {str(e)}")
            return False
    
    def test_ibm_quantum_connection(self):
        """Test IBM Quantum connection status"""
        print("\n🔍 Testing IBM Quantum Connection...")
        
        try:
            # Test if the app is running
            url = f"{self.base_url}/debug_quantum_manager"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                is_connected = data.get('is_connected', False)
                manager_exists = data.get('manager_exists', False)
                
                if manager_exists:
                    self.log_test("Quantum Manager", True, "Quantum manager exists")
                else:
                    self.log_test("Quantum Manager", False, "Quantum manager not found")
                
                if is_connected:
                    self.log_test("IBM Quantum Connection", True, "Connected to IBM Quantum")
                else:
                    self.log_test("IBM Quantum Connection", False, "Not connected to IBM Quantum")
                
                return is_connected
            else:
                self.log_test("IBM Quantum Connection", False, f"Debug endpoint failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("IBM Quantum Connection", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Dashboard Fix Tests")
        print("=" * 50)
        
        # Test basic connectivity
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code != 200:
                print("❌ Dashboard is not running. Please start the application first.")
                return False
        except:
            print("❌ Cannot connect to dashboard. Please start the application first.")
            return False
        
        # Run all tests
        self.test_dashboard_page()
        self.test_backends_api()
        self.test_jobs_api()
        self.test_dashboard_state_api()
        self.test_ibm_quantum_connection()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Show failed tests
        failed_tests = [result for result in self.test_results if not result['success']]
        if failed_tests:
            print("\n❌ Failed Tests:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['message']}")
        
        # Recommendations
        print("\n💡 Recommendations:")
        if not any(result['test'] == 'IBM Quantum Connection' and result['success'] for result in self.test_results):
            print("  - Set up IBM Quantum credentials using setup_ibm_quantum.py")
            print("  - Or run the dashboard in demo mode")
        
        if not any(result['test'] == 'Dashboard Page' and result['success'] for result in self.test_results):
            print("  - Update HTML templates to use dashboard_fixed.js")
        
        return passed == total

def main():
    """Main function"""
    print("🔧 Quantum Dashboard Fix Tester")
    print("=" * 50)
    
    # Check if server is running
    base_url = "http://localhost:10000"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    tester = DashboardTester(base_url)
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! Dashboard fixes are working correctly.")
        sys.exit(0)
    else:
        print("\n⚠️ Some tests failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
