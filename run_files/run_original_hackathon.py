#!/usr/bin/env python3
"""
Run the Original Hackathon Dashboard
====================================
This runs the exact same dashboard you had before the commit
"""

import os
import sys
import subprocess

def main():
    print("🚀 Quantum Spark - Original Hackathon Dashboard")
    print("=" * 50)
    print("📱 Restoring your exact dashboard from before the commit")
    print("🎯 This is the same dashboard you had originally")
    print("🌐 Will run on: http://localhost:10000")
    print("=" * 50)
    
    # Change to quantum_jobs_tracker directory
    os.chdir("quantum_jobs_tracker")
    
    # Run the simple hackathon app
    subprocess.run([sys.executable, "run_hackathon_simple.py"])

if __name__ == "__main__":
    main()
