#!/usr/bin/env python3
"""
Verification script for Bloch Sphere Integration
This script checks if all the necessary files are in place and the integration is ready.
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and report status."""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def check_directory_exists(dir_path, description):
    """Check if a directory exists and report status."""
    if os.path.isdir(dir_path):
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"❌ {description}: {dir_path} - NOT FOUND")
        return False

def main():
    print("🔍 Verifying Bloch Sphere Integration...")
    print("=" * 50)
    
    # Change to the quantum_jobs_tracker directory
    os.chdir(Path(__file__).parent)
    
    all_good = True
    
    # Check main integration files
    print("\n📁 Checking Integration Files:")
    all_good &= check_file_exists("static/hackathon_dashboard.js", "Modified Dashboard")
    all_good &= check_directory_exists("static/bloch-sphere-simulator", "Bloch Sphere Simulator")
    all_good &= check_file_exists("static/bloch-sphere-simulator/index.html", "Simulator Index")
    all_good &= check_directory_exists("static/3d-circuit-visualizer", "3D Circuit Visualizer")
    all_good &= check_file_exists("static/3d-circuit-visualizer/index.html", "3D Visualizer Index")
    all_good &= check_file_exists("test_bloch_integration.html", "Bloch Test Page")
    all_good &= check_file_exists("test_3d_circuit_integration.html", "3D Circuit Test Page")
    all_good &= check_file_exists("test_bloch_integration.py", "Test Server")
    all_good &= check_file_exists("BLOCH_SPHERE_INTEGRATION.md", "Documentation")
    
    # Check simulator key files
    print("\n🎯 Checking Simulator Key Files:")
    all_good &= check_file_exists("static/bloch-sphere-simulator/src/init.js", "Simulator Init")
    all_good &= check_file_exists("static/bloch-sphere-simulator/src/libs/three/three.min.js", "Three.js")
    all_good &= check_file_exists("static/bloch-sphere-simulator/css/main.css", "Simulator CSS")
    all_good &= check_file_exists("static/3d-circuit-visualizer/js/app.js", "3D Circuit App")
    all_good &= check_file_exists("static/3d-circuit-visualizer/styles.css", "3D Circuit CSS")
    all_good &= check_file_exists("static/3d-circuit-visualizer/three.min.js", "3D Circuit Three.js")
    
    # Check if the integration code is present
    print("\n🔧 Checking Integration Code:")
    try:
        with open("static/hackathon_dashboard.js", "r", encoding="utf-8") as f:
            content = f.read()
            
        if "bloch-sphere-iframe" in content:
            print("✅ Iframe integration code found")
        else:
            print("❌ Iframe integration code NOT found")
            all_good = False
            
        if "bloch-sphere-simulator/index.html" in content:
            print("✅ Bloch sphere simulator path reference found")
        else:
            print("❌ Bloch sphere simulator path reference NOT found")
            all_good = False
            
        if "3d-circuit-visualizer/index.html" in content:
            print("✅ 3D circuit visualizer path reference found")
        else:
            print("❌ 3D circuit visualizer path reference NOT found")
            all_good = False
            
    except Exception as e:
        print(f"❌ Error reading dashboard file: {e}")
        all_good = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 INTEGRATION VERIFICATION PASSED!")
        print("✅ All files are in place and ready to use.")
        print("\n📋 Next Steps:")
        print("   1. Run: python run_hackathon_dashboard.py")
        print("   2. Open the dashboard in your browser")
        print("   3. Add a bloch sphere widget and click fullscreen")
        print("   4. Add a 3D circuit widget and click fullscreen")
        print("\n🧪 Optional Testing:")
        print("   - Run: python test_bloch_integration.py (on port 8081)")
        print("   - Open: http://localhost:8081/test_bloch_integration.html")
        print("   - Open: http://localhost:8081/test_3d_circuit_integration.html")
    else:
        print("❌ INTEGRATION VERIFICATION FAILED!")
        print("Some files are missing or the integration is incomplete.")
        print("Please check the errors above and fix them.")
        sys.exit(1)

if __name__ == "__main__":
    main()
