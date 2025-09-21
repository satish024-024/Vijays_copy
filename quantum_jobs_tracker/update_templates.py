#!/usr/bin/env python3
"""
Script to update HTML templates to use the new dashboard_fixed.js
"""

import os
import re
from pathlib import Path

def update_template_file(file_path):
    """Update a single template file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace hackathon_dashboard.js with dashboard_fixed.js
        content = re.sub(
            r'src="/static/hackathon_dashboard\.js"',
            'src="/static/dashboard_fixed.js"',
            content
        )
        
        # Replace any other references to the old dashboard
        content = re.sub(
            r'new HackathonDashboard\(\)',
            'new EnhancedQuantumDashboard()',
            content
        )
        
        # Add initialization script if not present
        if 'new EnhancedQuantumDashboard()' in content and 'DOMContentLoaded' not in content:
            init_script = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the enhanced quantum dashboard
    window.dashboard = new EnhancedQuantumDashboard();
});
</script>
"""
            # Add before closing body tag
            content = re.sub(
                r'</body>',
                f'{init_script}\n</body>',
                content
            )
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
            return True
        else:
            print(f"⏭️  No changes needed: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main function"""
    print("🔄 Updating HTML templates to use dashboard_fixed.js")
    print("=" * 60)
    
    templates_dir = Path("templates")
    if not templates_dir.exists():
        print("❌ Templates directory not found")
        return
    
    # Find all HTML files
    html_files = list(templates_dir.glob("*.html"))
    
    if not html_files:
        print("❌ No HTML files found in templates directory")
        return
    
    updated_count = 0
    
    for html_file in html_files:
        if update_template_file(html_file):
            updated_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Summary: Updated {updated_count} out of {len(html_files)} files")
    
    if updated_count > 0:
        print("\n✅ Templates updated successfully!")
        print("💡 You can now test the dashboard with the new fixes.")
    else:
        print("\n⏭️  No templates needed updating.")

if __name__ == "__main__":
    main()
