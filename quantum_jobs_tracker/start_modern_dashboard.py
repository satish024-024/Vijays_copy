#!/usr/bin/env python3
"""
Start Modern Dashboard as Default
This script starts the quantum jobs tracker with the modern dashboard as the default
"""

import os
import sys
import webbrowser
import time
import subprocess
from pathlib import Path

def start_modern_dashboard():
    """Start the modern dashboard"""
    print("🚀 Starting Quantum Spark Modern Dashboard...")
    
    # Change to the correct directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if real_quantum_app.py exists
    if not Path("real_quantum_app.py").exists():
        print("❌ real_quantum_app.py not found!")
        return False
    
    try:
        # Start the server
        print("🔄 Starting quantum server...")
        process = subprocess.Popen([
            sys.executable, "real_quantum_app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(3)
        
        # Check if server is running
        try:
            import requests
            response = requests.get("http://localhost:5000/", timeout=5)
            if response.status_code == 200:
                print("✅ Server started successfully!")
                
                # Open modern dashboard in browser
                modern_dashboard_url = "http://localhost:5000/modern_dashboard"
                print(f"🌐 Opening modern dashboard: {modern_dashboard_url}")
                webbrowser.open(modern_dashboard_url)
                
                print("\n🎉 Modern Dashboard is now running!")
                print("📊 Dashboard URL: http://localhost:5000/modern_dashboard")
                print("🔧 Admin URL: http://localhost:5000/admin")
                print("\nPress Ctrl+C to stop the server")
                
                # Keep the script running
                try:
                    process.wait()
                except KeyboardInterrupt:
                    print("\n🛑 Stopping server...")
                    process.terminate()
                    process.wait()
                    print("✅ Server stopped")
                
                return True
            else:
                print(f"❌ Server returned status {response.status_code}")
                return False
        except ImportError:
            print("⚠️  requests library not available, cannot verify server status")
            print("🌐 Please open http://localhost:5000/modern_dashboard in your browser")
            process.wait()
            return True
        except Exception as e:
            print(f"❌ Error checking server: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("🎨 QUANTUM SPARK - MODERN DASHBOARD")
    print("=" * 60)
    print("This will start the quantum jobs tracker with the modern dashboard")
    print("as the default interface.")
    print()
    
    # Check if we're in the right directory
    if not Path("real_quantum_app.py").exists():
        print("❌ Please run this script from the quantum_jobs_tracker directory")
        print("   Current directory:", os.getcwd())
        return
    
    # Start the modern dashboard
    success = start_modern_dashboard()
    
    if not success:
        print("\n❌ Failed to start modern dashboard")
        print("Please check the error messages above and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()
