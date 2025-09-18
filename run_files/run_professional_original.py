#!/usr/bin/env python3
"""
Run the Professional Dashboard
==============================
Clean professional interface with advanced analytics
"""

import os
import sys
import subprocess

def main():
    print("🚀 Quantum Spark - Professional Dashboard")
    print("=" * 50)
    print("📱 Professional Quantum Analytics Dashboard")
    print("🎯 Clean, professional interface with advanced features")
    print("🌐 Will run on: http://localhost:10001")
    print("=" * 50)
    
    # Change to quantum_jobs_tracker directory
    os.chdir("quantum_jobs_tracker")
    
    # Run the professional app
    subprocess.run([sys.executable, "run_professional_simple.py"])

if __name__ == "__main__":
    main()
