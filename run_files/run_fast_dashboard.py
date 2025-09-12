#!/usr/bin/env python3
"""
🚀 Fast Quantum Dashboard Launcher
Ultra-fast loading quantum dashboard with instant initialization
"""

import os
import sys
import webbrowser
import time
import threading
from pathlib import Path

def main():
    print("⚡ Fast Quantum Dashboard Launcher")
    print("=" * 50)
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"📁 Project directory: {project_root}")
    
    # Check if the main app exists
    app_file = project_root / "quantum_jobs_tracker" / "real_quantum_app.py"
    if not app_file.exists():
        print(f"❌ Error: {app_file} not found!")
        print("Please make sure you're running this from the correct directory.")
        return
    
    print("✅ Found quantum app file")
    
    # Start the Flask server
    print("🚀 Starting Fast Quantum Dashboard server...")
    print("📡 Server will be available at: http://localhost:5000/fast")
    print("⚡ Fast mode: No IBM Quantum token required!")
    print("🎯 Features: Instant loading, demo data, all quantum widgets")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://localhost:5000/fast")
        print("🌐 Browser opened to Fast Dashboard")
    
    # Start browser opening in background
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run the Flask app
    try:
        os.system("python quantum_jobs_tracker/real_quantum_app.py")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
