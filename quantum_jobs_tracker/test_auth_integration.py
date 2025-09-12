#!/usr/bin/env python3
"""
Test script to verify authentication integration
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_auth_imports():
    """Test if authentication modules can be imported"""
    print("🔍 Testing authentication module imports...")

    try:
        from oauth_auth import IBMQuantumOAuth
        print("✅ OAuth module imported successfully")
    except ImportError as e:
        print(f"❌ OAuth module import failed: {e}")

    try:
        from ibm_cloud_auth import IBMCloudIAM
        print("✅ IBM Cloud IAM module imported successfully")
    except ImportError as e:
        print(f"❌ IBM Cloud IAM module import failed: {e}")

    try:
        from secure_token_manager import SecureTokenManager
        print("✅ Secure Token Manager imported successfully")
    except ImportError as e:
        print(f"❌ Secure Token Manager import failed: {e}")

    try:
        from auth_integration import QuantumAuthManager
        print("✅ Authentication Integration imported successfully")
    except ImportError as e:
        print(f"❌ Authentication Integration import failed: {e}")

def test_flask_integration():
    """Test Flask app integration"""
    print("\n🔍 Testing Flask integration...")

    try:
        from real_quantum_app import app, WATSONX_AUTH_AVAILABLE
        print(f"✅ Flask app imported successfully")
        print(f"   watsonx.ai authentication available: {WATSONX_AUTH_AVAILABLE}")

        if WATSONX_AUTH_AVAILABLE:
            print("✅ watsonx.ai authentication system is active")
        else:
            print("⚠️  Using fallback authentication system")

    except ImportError as e:
        print(f"❌ Flask integration failed: {e}")

def test_template_access():
    """Test if authentication templates are accessible"""
    print("\n🔍 Testing template access...")

    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    templates = ['multi_auth.html', 'token_input.html']

    for template in templates:
        template_path = os.path.join(template_dir, template)
        if os.path.exists(template_path):
            print(f"✅ Template {template} found")
        else:
            print(f"❌ Template {template} missing")

def main():
    """Run all tests"""
    print("🚀 Testing Authentication Integration")
    print("=" * 50)

    test_auth_imports()
    test_flask_integration()
    test_template_access()

    print("\n" + "=" * 50)
    print("🎯 Integration test complete!")
    print("\n📋 Next steps:")
    print("1. Install requirements: pip install -r requirements.txt")
    print("2. Run the app: python real_quantum_app.py")
    print("3. Visit http://localhost:5000 to see new authentication")
    print("4. If issues occur, check console for detailed error messages")

if __name__ == '__main__':
    main()
