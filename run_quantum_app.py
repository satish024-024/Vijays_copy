#!/usr/bin/env python3
"""
Quantum Jobs Tracker Launcher
This script launches the quantum application with dependency checks.
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        "qiskit",
        "qiskit_ibm_provider",
        "qiskit_ibm_runtime",
        "flask",
        "numpy",
        "matplotlib"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n🔧 Please run the setup script first:")
        print("   python setup_ibm_quantum.py")
        return False
    
    print("✅ All required packages are installed")
    return True

def main():
    """Main launcher function"""
    print("🚀 Quantum Jobs Tracker Launcher")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if the main app file exists
    app_path = "quantum_jobs_tracker/real_quantum_app.py"
    if not os.path.exists(app_path):
        print(f"❌ Application file not found: {app_path}")
        print("Please ensure you're in the correct directory")
        sys.exit(1)
    
    print("🎯 Launching Quantum Jobs Tracker...")
    print("📱 The application will open at: http://localhost:10000")
    print("🔐 Enter your IBM Quantum API token in the web interface")
    print("\n💡 To stop the application, press Ctrl+C")
    print("=" * 40)
    
    try:
        # Launch the application
        subprocess.run([sys.executable, app_path], check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Application failed to start: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"\n❌ Python executable not found: {sys.executable}")
        sys.exit(1)

if __name__ == "__main__":
    main()
