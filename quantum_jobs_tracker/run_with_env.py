#!/usr/bin/env python3
"""
Quantum Jobs Tracker - Clean Environment Runner
This script activates the virtual environment and runs the Flask application
"""

import os
import sys
import subprocess
import platform

def main():
    # Get the directory paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    print("🚀 Starting Quantum Jobs Tracker with Clean Qiskit Environment...")
    print(f"📁 Project root: {project_root}")
    print(f"📁 Script directory: {script_dir}")

    # Check if virtual environment exists
    venv_path = os.path.join(project_root, 'quantum_env')
    if not os.path.exists(venv_path):
        print("❌ Virtual environment not found!")
        print("Please run the following commands first:")
        print(f"cd {project_root}")
        print("python -m venv quantum_env")
        print("quantum_env\\Scripts\\activate")
        print("pip install qiskit-ibm-runtime qiskit-ibm-provider flask")
        return 1

    # Activate virtual environment and run Flask app
    if platform.system() == 'Windows':
        # Windows
        activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat')
        flask_script = os.path.join(script_dir, 'real_quantum_app.py')

        print("🔧 Activating virtual environment (Windows)...")
        print("🌐 Starting Flask server...")

        # Use subprocess to run the batch file and Flask app
        try:
            subprocess.run([activate_script, '&&', sys.executable, flask_script],
                         shell=True, cwd=script_dir)
        except KeyboardInterrupt:
            print("\n👋 Server stopped by user")
        except Exception as e:
            print(f"❌ Error running server: {e}")
            return 1
    else:
        # Linux/Mac
        activate_script = os.path.join(venv_path, 'bin', 'activate')
        flask_script = os.path.join(script_dir, 'real_quantum_app.py')

        print("🔧 Activating virtual environment (Unix)...")
        print("🌐 Starting Flask server...")

        try:
            # Source the activation script and run Flask
            cmd = f"source {activate_script} && {sys.executable} {flask_script}"
            subprocess.run(cmd, shell=True, executable='/bin/bash', cwd=script_dir)
        except KeyboardInterrupt:
            print("\n👋 Server stopped by user")
        except Exception as e:
            print(f"❌ Error running server: {e}")
            return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
