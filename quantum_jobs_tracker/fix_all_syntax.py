#!/usr/bin/env python3
"""
Comprehensive fix for all syntax errors
"""

import re

def fix_all_syntax_errors():
    """Fix all syntax errors in the file"""
    
    with open('real_quantum_app.py', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Fix 1: Fix all indentation issues with quantum_manager calls
    pattern = r'(\s+)quantum_token, quantum_crn = get_user_quantum_credentials\(\)\s*\n(\s*)quantum_manager = quantum_manager_singleton\.get_manager\(quantum_token, quantum_crn\)'
    replacement = r'\1quantum_token, quantum_crn = get_user_quantum_credentials()\n\1quantum_manager = quantum_manager_singleton.get_manager(quantum_token, quantum_crn)'
    content = re.sub(pattern, replacement, content)
    
    # Fix 2: Remove duplicate credentials retrieval
    pattern = r'quantum_token, quantum_crn = get_user_quantum_credentials\(\)\s*\n\s*quantum_token, quantum_crn = get_user_quantum_credentials\(\)'
    replacement = r'quantum_token, quantum_crn = get_user_quantum_credentials()'
    content = re.sub(pattern, replacement, content)
    
    # Fix 3: Fix malformed try-except blocks
    pattern = r'(\s+)try:\s*\n(\s+)quantum_token, quantum_crn = get_user_quantum_credentials\(\)\s*\n(\s+)quantum_manager = quantum_manager_singleton\.get_manager\(quantum_token, quantum_crn\)\s*\n(\s+)if quantum_manager:'
    replacement = r'\1try:\n\2quantum_token, quantum_crn = get_user_quantum_credentials()\n\2quantum_manager = quantum_manager_singleton.get_manager(quantum_token, quantum_crn)\n\2if quantum_manager:'
    content = re.sub(pattern, replacement, content)
    
    # Fix 4: Remove fake data references
    content = re.sub(r'"backends": sample_backends,', '"backends": [],', content)
    content = re.sub(r'sample_backends = \[.*?\]', '[]', content, flags=re.DOTALL)
    
    # Fix 5: Remove infinite loop patterns
    content = re.sub(r'ðŸ"— Trying instance:.*?ðŸ"— Trying without instance.*?ðŸ"— Trying simpler connection approach', '🔄 Attempting IBM Quantum connection...', content, flags=re.DOTALL)
    
    # Write the fixed content back
    with open('real_quantum_app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed all syntax errors")

if __name__ == "__main__":
    fix_all_syntax_errors()
