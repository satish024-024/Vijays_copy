#!/usr/bin/env python3
"""
Test script for Bloch Sphere Integration
This script serves a test page to verify the iframe integration works correctly.
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow iframe embedding
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    PORT = 8081
    
    # Change to the quantum_jobs_tracker directory
    os.chdir(Path(__file__).parent)
    
    print("🚀 Starting Bloch Sphere Integration Test Server...")
    print(f"📡 Server running on http://localhost:{PORT}")
    print("🌐 Opening test page in browser...")
    
    # Open the test page in the browser
    webbrowser.open(f'http://localhost:{PORT}/test_bloch_integration.html')
    
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"✅ Server started successfully!")
        print("📋 Test Instructions:")
        print("   1. Click 'Test Iframe Integration' to load the bloch sphere")
        print("   2. Click 'Test Fullscreen Mode' to test fullscreen functionality")
        print("   3. Press ESC to exit fullscreen")
        print("   4. Press Ctrl+C to stop the server")
        print("\n" + "="*60)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            print("✅ Integration test completed!")

if __name__ == "__main__":
    main()
