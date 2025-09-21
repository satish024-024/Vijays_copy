#!/usr/bin/env python3
"""
Quick fix for syntax errors
"""

# Fix the specific syntax error by removing the problematic except block
with open('real_quantum_app.py', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

# Find and fix the problematic except block
for i, line in enumerate(lines):
    if 'except Exception as e:' in line and 'Error getting real dashboard state' in lines[i+1]:
        # Remove the problematic except block and replace with proper error handling
        lines[i] = '    except Exception as e:\n'
        lines[i+1] = '        print(f"⚠️ Error getting real dashboard state: {e}")\n'
        if i+2 < len(lines):
            lines[i+2] = '        return jsonify({"error": "Failed to get dashboard state", "message": str(e), "real_data": False}), 500\n'
        break

# Write the fixed content back
with open('real_quantum_app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed syntax error")
