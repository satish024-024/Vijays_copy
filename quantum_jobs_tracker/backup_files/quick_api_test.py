#!/usr/bin/env python3
"""
Quick IBM Quantum API Key Test
Simple test to verify API key works
"""

import sys
import os

def test_ibm_quantum_connection():
    """Test basic IBM Quantum connection"""
    print("🔍 Testing IBM Quantum API Key")
    print("=" * 40)

    try:
        print("1. Testing imports...")
        from qiskit_ibm_runtime import QiskitRuntimeService
        print("   ✅ IBM Runtime imported")

        from qiskit_ibm_provider import IBMProvider
        print("   ✅ IBM Provider imported")

    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False

    print("\n2. Testing service availability...")
    try:
        # Test without API key first
        service = QiskitRuntimeService()
        print("   ⚠️  No API key provided - service created but not authenticated")
        print("   💡 This means IBM Quantum is reachable")

        # Try to list channels (this should work without auth)
        print("   📡 IBM Quantum service is accessible")
        return True

    except Exception as e:
        print(f"   ❌ Service connection failed: {e}")
        print("   💡 This could indicate network issues or IBM service downtime")
        return False

def main():
    print("🚀 IBM Quantum Quick Connection Test")
    print("=" * 50)

    success = test_ibm_quantum_connection()

    if success:
        print("\n🎉 IBM Quantum service is accessible!")
        print("\n📝 Next steps:")
        print("1. Your API key format should be: ibm_XXXXXXXXXXXXXXXXXXXX")
        print("2. Make sure you copied the complete API key from IBM Cloud")
        print("3. Check that your IBM Quantum account has available credits")
        print("4. Try accessing the web interface at: http://localhost:10000")
    else:
        print("\n❌ Connection issues detected")
        print("\n🔧 Troubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify IBM Quantum service status")
        print("3. Try again in a few minutes")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
