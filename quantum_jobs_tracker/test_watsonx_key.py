#!/usr/bin/env python3
"""
watsonx.ai API Key Validation Test
Test your watsonx.ai API key before using it in the quantum platform
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ibm_cloud_auth import test_watsonx_api_key

def main():
    print("🔑 watsonx.ai API Key Validator")
    print("=" * 50)

    # Get API key from user
    api_key = input("\nEnter your watsonx.ai API key: ").strip()

    if not api_key:
        print("❌ No API key provided")
        return

    print("\n🔍 Testing watsonx.ai API key...")
    print("-" * 30)

    # Test the API key
    result = test_watsonx_api_key(api_key)

    if result['success']:
        print("✅ SUCCESS!")
        print(f"   Token Type: {result.get('token_type', 'N/A')}")
        print(f"   Expires In: {result.get('expires_in', 'N/A')} seconds")
        print(f"   watsonx URL: {result.get('watsonx_url', 'N/A')}")
        print("\n🎉 Your watsonx.ai API key is valid and ready to use!")
    else:
        print("❌ VALIDATION FAILED")
        print(f"   Error: {result['error']}")
        print(f"   Guidance: {result.get('guidance', 'Please check your API key')}")

        print("\n🔧 Troubleshooting Tips:")
        print("   1. Make sure you're using a watsonx.ai API key (not IBM Quantum)")
        print("   2. Check if your API key has expired")
        print("   3. Verify you have watsonx.ai service access in IBM Cloud")
        print("   4. Try generating a new API key if the current one doesn't work")

if __name__ == "__main__":
    main()
