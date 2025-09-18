#!/usr/bin/env python3
"""
Database Testing Script
Tests database connectivity, table structure, and data integrity
"""

import sqlite3
import os
from user_auth import user_auth

def test_database():
    """Test database functionality"""
    print("🔍 Testing Database System...")
    
    # Check if database file exists
    db_path = "quantum_data.db"
    if os.path.exists(db_path):
        print(f"✅ Database file exists: {db_path}")
        file_size = os.path.getsize(db_path)
        print(f"   📊 Database size: {file_size} bytes")
    else:
        print(f"❌ Database file not found: {db_path}")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("✅ Database connection successful")
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Database tables: {[table[0] for table in tables]}")
        
        # Check users table structure
        if ('users',) in tables:
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()
            print("👥 Users table columns:")
            for col in columns:
                print(f"   - {col[1]} ({col[2]})")
            
            # Check user count
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"   📊 Total users: {user_count}")
            
            # Check if any users have IBM Quantum credentials
            cursor.execute("SELECT COUNT(*) FROM users WHERE api_key IS NOT NULL AND api_key != ''")
            users_with_creds = cursor.fetchone()[0]
            print(f"   🔑 Users with IBM Quantum credentials: {users_with_creds}")
            
        else:
            print("❌ Users table not found")
        
        # Test user authentication system
        print("\n🔐 Testing User Authentication System...")
        
        # Test user registration
        test_email = "test@example.com"
        test_password = "testpass123"
        test_api_key = "test_api_key_12345"
        test_crn = "test_crn_67890"
        
        # Check if test user exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (test_email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"   ⚠️  Test user already exists, cleaning up...")
            cursor.execute("DELETE FROM users WHERE email = ?", (test_email,))
            conn.commit()
        
        # Test registration
        success, message = user_auth.register_user(test_email, test_password, test_api_key, test_crn)
        if success:
            print(f"   ✅ User registration test: {message}")
        else:
            print(f"   ❌ User registration test failed: {message}")
            conn.close()
            return False
        
        # Test login
        success, message, token, api_key, crn = user_auth.login_user(test_email, test_password)
        if success:
            print(f"   ✅ User login test: {message}")
            print(f"   🔑 Retrieved API key: {api_key[:10]}...")
            print(f"   🏢 Retrieved CRN: {crn[:15]}...")
        else:
            print(f"   ❌ User login test failed: {message}")
            conn.close()
            return False
        
        # Test credential retrieval
        user_id = user_auth.verify_token(token)['user_id']
        retrieved_api_key, retrieved_crn = user_auth.get_user_credentials(user_id)
        if retrieved_api_key == test_api_key and retrieved_crn == test_crn:
            print(f"   ✅ Credential retrieval test: Success")
        else:
            print(f"   ❌ Credential retrieval test: Failed")
            conn.close()
            return False
        
        # Clean up test user
        cursor.execute("DELETE FROM users WHERE email = ?", (test_email,))
        conn.commit()
        print(f"   🧹 Test user cleaned up")
        
        conn.close()
        print("✅ Database testing completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Database testing failed: {e}")
        return False

if __name__ == "__main__":
    success = test_database()
    if success:
        print("\n🎉 All database tests passed!")
    else:
        print("\n💥 Database tests failed!")
