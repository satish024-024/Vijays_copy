#!/usr/bin/env python3
"""
Simple Python launcher for Quantum Advantage Research Platform
This avoids PowerShell syntax issues
"""

import os
import sys
import subprocess
import time

def main():
    print("🚀 Quantum Advantage Research Platform Launcher")
    print("=" * 50)

    # Check if we're in the right directory
    current_dir = os.getcwd()
    if not os.path.exists("quantum_env"):
        print("❌ quantum_env directory not found!")
        print("   Please run this from the project root directory")
        input("Press Enter to exit...")
        return

    if not os.path.exists("quantum_jobs_tracker"):
        print("❌ quantum_jobs_tracker directory not found!")
        print("   Please run this from the project root directory")
        input("Press Enter to exit...")
        return

    print("✅ Project structure verified")

    # Activate virtual environment
    print("\n📦 Activating virtual environment...")
    activate_script = os.path.join("quantum_env", "Scripts", "activate.bat")

    if os.name == 'nt':  # Windows
        # Use subprocess to run the activation and then Python
        print("🔧 Starting Flask application...")

        # Change to quantum_jobs_tracker directory
        os.chdir("quantum_jobs_tracker")

        # Run the Flask app
        print("🌐 Access your platform at:")
        print("   Main Dashboard: http://localhost:10000")
        print("   Research Platform: http://localhost:10000/quantum-research")
        print("\n" + "=" * 50)

        try:
            subprocess.run([sys.executable, "real_quantum_app.py"], check=True)
        except KeyboardInterrupt:
            print("\n👋 Application stopped by user")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Application exited with error: {e}")
            input("Press Enter to exit...")

    else:
        print("❌ This launcher is designed for Windows only")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
