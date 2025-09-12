#!/usr/bin/env python3
"""
Test script to demonstrate real IBM Quantum job data integration
This script shows how to use the real job data you provided with the dashboard
"""

from qiskit_ibm_runtime import QiskitRuntimeService
import json

def test_real_job_integration():
    """Test the real job integration with the dashboard"""
    
    print("🔬 Testing Real IBM Quantum Job Integration")
    print("=" * 50)
    
    # Your real job data
    job_id = "d2pr2olpoa4c73c94kn0"
    instance_crn = "crn:v1:bluemix:public:quantum-computing:us-east:a/22643a9008454fa2af1809e248bb4f72:61c1f88e-f36b-4c06-9eb1-3600e3be780f::"
    
    try:
        print(f"📡 Connecting to IBM Quantum with job ID: {job_id}")
        
        # Initialize the service
        service = QiskitRuntimeService(
            channel='ibm_quantum_platform',
            instance=instance_crn
        )
        
        print("✅ Connected to IBM Quantum Runtime Service")
        
        # Get the job
        job = service.job(job_id)
        print(f"📊 Retrieved job: {job_id}")
        
        # Get job result
        job_result = job.result()
        print("📈 Retrieved job result")
        
        # Extract measurement data
        counts = {}
        try:
            # Try different methods to get counts
            if hasattr(job_result, 'get_counts'):
                counts = job_result.get_counts()
            elif hasattr(job_result, 'data') and hasattr(job_result.data, 'get_counts'):
                counts = job_result.data.get_counts()
            else:
                # Try to get counts from pub results
                if hasattr(job_result, '__getitem__'):
                    for i, pub_result in enumerate(job_result):
                        if hasattr(pub_result, 'data') and hasattr(pub_result.data, 'get_counts'):
                            counts = pub_result.data.get_counts()
                            break
            
            print(f"📊 Measurement outcomes: {len(counts)} different results")
            print("🔍 Sample measurement data:")
            for state, count in list(counts.items())[:5]:  # Show first 5
                print(f"   |{state}⟩: {count} counts")
            
        except Exception as e:
            print(f"⚠️ Could not extract measurement data: {e}")
            counts = {}
        
        # Get job metadata
        backend_name = "unknown"
        status = "unknown"
        shots = 1024
        
        try:
            if hasattr(job, 'backend') and callable(job.backend):
                backend_obj = job.backend()
                backend_name = getattr(backend_obj, 'name', 'unknown')
            elif hasattr(job, 'backend_name'):
                backend_name = job.backend_name
            
            if hasattr(job, 'status') and callable(job.status):
                status_obj = job.status()
                status = str(status_obj)
            elif hasattr(job, 'status'):
                status = str(job.status)
            
            if hasattr(job, 'shots'):
                shots = job.shots
                
        except Exception as e:
            print(f"⚠️ Could not retrieve job metadata: {e}")
        
        # Create dashboard-compatible result data
        result_data = {
            "job_id": job_id,
            "backend": backend_name,
            "status": status,
            "execution_time": 0,  # Will be calculated if available
            "created_time": 0,    # Will be calculated if available
            "completed_time": 0,  # Will be calculated if available
            "shots": shots,
            "counts": counts,
            "real_data": True,
            "algorithm_type": "real_quantum_algorithm",
            "scenario_name": f"Real Job {job_id}",
            "description": f"Real quantum job executed on {backend_name}",
            "total_shots": shots,
            "probability_sum": round(sum(counts.values()) / shots * 100, 1) if shots > 0 else 0
        }
        
        print("\n🎯 Dashboard-Compatible Result Data:")
        print("=" * 50)
        print(f"Job ID: {result_data['job_id']}")
        print(f"Backend: {result_data['backend']}")
        print(f"Status: {result_data['status']}")
        print(f"Shots: {result_data['shots']}")
        print(f"Measurement Outcomes: {len(result_data['counts'])}")
        print(f"Total Probability: {result_data['probability_sum']}%")
        print(f"Real Data: {result_data['real_data']}")
        
        # Save to JSON file for dashboard testing
        with open('real_job_data.json', 'w') as f:
            json.dump(result_data, f, indent=2)
        
        print(f"\n💾 Result data saved to 'real_job_data.json'")
        print("🚀 This data can now be used with the dashboard!")
        
        return result_data
        
    except Exception as e:
        print(f"❌ Error testing real job integration: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")
        return None

if __name__ == "__main__":
    test_real_job_integration()
