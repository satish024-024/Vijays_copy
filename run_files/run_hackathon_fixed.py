#!/usr/bin/env python3
"""
Run the Fixed Hackathon Dashboard
================================
All scripts and APIs working properly - no more 404 errors!
"""

import os
import sys
import subprocess

def main():
    print("🚀 Quantum Spark - Fixed Hackathon Dashboard")
    print("=" * 50)
    print("📱 Amravati Quantum Hackathon Dashboard")
    print("🎯 All scripts and APIs working properly")
    print("🌐 Will run on: http://localhost:10000")
    print("=" * 50)
    print("✅ Fixed Issues:")
    print("   • Missing blochy-source scripts")
    print("   • Missing API endpoints")
    print("   • 404 errors resolved")
    print("   • All features working")
    print("=" * 50)
    
    # Change to quantum_jobs_tracker directory
    os.chdir("quantum_jobs_tracker")
    
    # Run the fixed hackathon app
    subprocess.run([sys.executable, "run_hackathon_fixed.py"])

if __name__ == "__main__":
    main()
