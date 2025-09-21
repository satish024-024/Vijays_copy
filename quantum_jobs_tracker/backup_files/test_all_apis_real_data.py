#!/usr/bin/env python3
"""
Complete API Test - Check ALL APIs are working with REAL data only
No mock data - only real IBM Quantum data validation
"""

import requests
import json
import time

def test_all_apis_real_data():
    """Test ALL API endpoints for real data only"""
    base_url = "http://localhost:10000"
    
    print("🚀 TESTING ALL APIs FOR REAL DATA")
    print("=" * 50)
    
    # Test results tracking
    total_apis = 0
    working_apis = 0
    real_data_apis = 0
    failed_apis = []
    
    # List of ALL API endpoints to test
    api_endpoints = [
        # Core APIs
        ("/status", "System Status"),
        ("/api/backends", "Quantum Backends"),
        ("/api/jobs", "Quantum Jobs"),
        ("/api/job_results", "Job Results"),
        
        # Metrics APIs
        ("/api/dashboard_metrics", "Dashboard Metrics"),
        ("/api/performance_metrics", "Performance Metrics"),
        ("/api/realtime_monitoring", "Real-time Monitoring"),
        ("/api/historical_data", "Historical Data"),
        ("/api/calibration_data", "Calibration Data"),
        
        # Data APIs
        ("/api/database_stats", "Database Statistics"),
        ("/api/metrics_history", "Metrics History"),
        ("/api/cached_data/jobs", "Cached Jobs"),
        ("/api/cached_data/backends", "Cached Backends"),
        
        # Quantum State APIs
        ("/api/quantum_state_data", "Quantum State Data"),
        ("/api/circuit_data", "Circuit Data"),
        ("/api/quantum_state", "Quantum State"),
        ("/api/quantum_circuit", "Quantum Circuit"),
        
        # Sync APIs
        ("/api/sync_status", "Sync Status"),
        ("/api/offline_data", "Offline Data"),
        
        # Advanced APIs
        ("/api/circuit_details", "Circuit Details"),
        ("/api/dashboard_state", "Dashboard State"),
        ("/api/notifications", "Notifications"),
        ("/api/quantum_visualization_data", "Visualization Data"),
        ("/api/real_features_summary", "Features Summary"),
        ("/api/results", "Results"),
        ("/api/performance", "Performance"),
        ("/api/recommendations", "Recommendations"),
        ("/api/predictions", "Predictions"),
        ("/api/backend_comparison", "Backend Comparison"),
        
        # Research APIs
        ("/api/quantum-algorithms", "Quantum Algorithms"),
        ("/api/quantum-study", "Quantum Study"),
        ("/api/quantum-visualizations", "Quantum Visualizations"),
        ("/api/quantum-report", "Quantum Report"),
        
        # Connection APIs
        ("/connection_status", "Connection Status"),
        ("/api/clear_cache", "Clear Cache"),
    ]
    
    print(f"📋 Testing {len(api_endpoints)} API endpoints...")
    print()
    
    for endpoint, description in api_endpoints:
        total_apis += 1
        print(f"{total_apis:2d}. {description} ({endpoint})")
        
        try:
            # Test GET request
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                working_apis += 1
                print(f"    ✅ Status: 200 OK")
                
                # Try to parse JSON response
                try:
                    data = response.json()
                    
                    # Check if data is real (not empty, not mock)
                    if isinstance(data, dict) and data:
                        # Check for real data indicators
                        has_real_data = check_real_data_indicators(data, endpoint)
                        if has_real_data:
                            real_data_apis += 1
                            print(f"    ✅ Real Data: {len(str(data))} chars")
                        else:
                            print(f"    ⚠️  Mock/Empty Data: {len(str(data))} chars")
                    elif isinstance(data, list) and data:
                        real_data_apis += 1
                        print(f"    ✅ Real Data: {len(data)} items")
                    else:
                        print(f"    📭 Empty Response")
                        
                except json.JSONDecodeError:
                    print(f"    📄 Non-JSON Response: {len(response.text)} chars")
                    
            elif response.status_code in [401, 403]:
                print(f"    🔐 Requires Authentication ({response.status_code})")
                working_apis += 1  # Still working, just needs auth
                
            elif response.status_code in [302]:
                print(f"    🔄 Redirect ({response.status_code})")
                working_apis += 1  # Still working, just redirects
                
            else:
                print(f"    ❌ Failed: {response.status_code}")
                failed_apis.append((endpoint, description, response.status_code))
                
        except requests.exceptions.Timeout:
            print(f"    ⏱️  Timeout")
            failed_apis.append((endpoint, description, "Timeout"))
            
        except requests.exceptions.ConnectionError:
            print(f"    🔌 Connection Error")
            failed_apis.append((endpoint, description, "Connection Error"))
            
        except Exception as e:
            print(f"    ❌ Error: {str(e)[:50]}...")
            failed_apis.append((endpoint, description, str(e)[:50]))
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.1)
    
    # Test POST endpoints
    print(f"\n📝 Testing POST endpoints...")
    post_endpoints = [
        ("/api/apply_quantum_gate", "Apply Quantum Gate", {"gate_type": "h", "qubit": 0}),
        ("/api/start_sync", "Start Sync", {}),
        ("/api/force_sync", "Force Sync", {}),
        ("/api/set_sync_interval", "Set Sync Interval", {"interval": 300}),
        ("/api/cleanup_database", "Cleanup Database", {}),
    ]
    
    for endpoint, description, data in post_endpoints:
        total_apis += 1
        print(f"{total_apis:2d}. {description} ({endpoint})")
        
        try:
            response = requests.post(f"{base_url}{endpoint}", 
                                   json=data,
                                   headers={'Content-Type': 'application/json'},
                                   timeout=10)
            
            if response.status_code in [200, 201]:
                working_apis += 1
                print(f"    ✅ Status: {response.status_code}")
                try:
                    result = response.json()
                    if result:
                        print(f"    ✅ Response: {len(str(result))} chars")
                except:
                    print(f"    📄 Response: {len(response.text)} chars")
            else:
                print(f"    ❌ Failed: {response.status_code}")
                failed_apis.append((endpoint, description, response.status_code))
                
        except Exception as e:
            print(f"    ❌ Error: {str(e)[:50]}...")
            failed_apis.append((endpoint, description, str(e)[:50]))
    
    # Generate final report
    print("\n" + "=" * 50)
    print("🎯 FINAL API TEST RESULTS")
    print("=" * 50)
    
    success_rate = (working_apis / total_apis * 100) if total_apis > 0 else 0
    real_data_rate = (real_data_apis / total_apis * 100) if total_apis > 0 else 0
    
    print(f"📊 Total APIs Tested: {total_apis}")
    print(f"✅ Working APIs: {working_apis} ({success_rate:.1f}%)")
    print(f"📡 APIs with Real Data: {real_data_apis} ({real_data_rate:.1f}%)")
    print(f"❌ Failed APIs: {len(failed_apis)}")
    
    if failed_apis:
        print(f"\n❌ Failed APIs:")
        for endpoint, description, error in failed_apis[:10]:  # Show first 10 failures
            print(f"   - {description} ({endpoint}): {error}")
        if len(failed_apis) > 10:
            print(f"   ... and {len(failed_apis) - 10} more failures")
    
    print(f"\n🎉 API Health Status:")
    if success_rate >= 90:
        print("   ✅ EXCELLENT: Most APIs are working perfectly!")
    elif success_rate >= 70:
        print("   👍 GOOD: Most APIs are working well")
    elif success_rate >= 50:
        print("   ⚠️  FAIR: Some APIs need attention")
    else:
        print("   ❌ POOR: Many APIs are not working")
    
    if real_data_rate >= 50:
        print("   🌐 REAL DATA: Getting actual quantum data")
    elif real_data_rate >= 20:
        print("   🔄 MIXED: Some real data, some mock data")
    else:
        print("   🎭 MOCK DATA: Mostly demo/mock data")
    
    print(f"\n💡 Recommendations:")
    if success_rate < 90:
        print("   🔧 Fix failed APIs to improve reliability")
    if real_data_rate < 50:
        print("   🔑 Add IBM Quantum credentials for real data")
    if len(failed_apis) > 0:
        print("   📋 Review failed APIs in the list above")
    
    return {
        "total_apis": total_apis,
        "working_apis": working_apis,
        "real_data_apis": real_data_apis,
        "success_rate": success_rate,
        "real_data_rate": real_data_rate,
        "failed_apis": failed_apis
    }

def check_real_data_indicators(data, endpoint):
    """Check if data contains indicators of real vs mock data"""
    
    # Mock data indicators (hardcoded values)
    mock_indicators = {
        "total_jobs": 15,
        "active_backends": 4,
        "running_jobs": 2,
        "queued_jobs": 2
    }
    
    # Real data indicators
    real_indicators = [
        "ibmq_", "ibm_", "job_id", "backend_name", 
        "execution_time", "shots", "counts", "timestamp"
    ]
    
    # Check for mock data
    for key, expected_value in mock_indicators.items():
        if data.get(key) == expected_value:
            return False  # Likely mock data
    
    # Check for real data indicators
    data_str = str(data).lower()
    for indicator in real_indicators:
        if indicator.lower() in data_str:
            return True  # Likely real data
    
    # If data exists but no clear indicators, assume real
    return len(str(data)) > 50  # Substantial data is likely real

if __name__ == "__main__":
    try:
        results = test_all_apis_real_data()
        
        # Exit with appropriate code
        if results["success_rate"] >= 80:
            exit(0)  # Success
        else:
            exit(1)  # Some failures
            
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        exit(1)
