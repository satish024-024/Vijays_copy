#!/usr/bin/env python3
"""
Run the Stable Hackathon Dashboard
=================================
Fixed version - no more flickering or continuous loading!
"""

import os
import sys
import subprocess

def main():
    print("🚀 Quantum Spark - Stable Hackathon Dashboard")
    print("=" * 50)
    print("📱 Amravati Quantum Hackathon Dashboard")
    print("🎯 Fixed: No more flickering or continuous loading!")
    print("🌐 Will run on: http://localhost:10000")
    print("=" * 50)
    print("✅ Fixed Issues:")
    print("   • Disabled real-time updates")
    print("   • Fixed refresh intervals")
    print("   • Cached API responses")
    print("   • No more flickering")
    print("   • Stable loading")
    print("=" * 50)
    
    # Change to quantum_jobs_tracker directory
    os.chdir("quantum_jobs_tracker")
    
    # Run the fixed hackathon app
    subprocess.run([sys.executable, "hackathon_dashboard_app.py"])

if __name__ == "__main__":
    main()
