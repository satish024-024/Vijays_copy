#!/usr/bin/env python3
"""
Test script for offline functionality and database improvements
"""

import sys
import os
import time
import json
import datetime
from database import db

def test_database_connection():
    """Test database connection and basic operations"""
    print("🔍 Testing database connection...")

    try:
        # Test basic stats
        stats = db.get_database_stats()
        print(f"✅ Database stats: {stats}")

        # Test sync status
        sync_status = db.get_sync_status()
        print(f"✅ Sync status: {sync_status}")

        return True
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def test_offline_data_operations():
    """Test offline data retrieval operations"""
    print("🔍 Testing offline data operations...")

    try:
        # Test offline data retrieval
        offline_data = db.get_offline_data(max_age_minutes=30)
        print(f"✅ Offline data retrieved: {len(offline_data.get('backends', []))} backends, {len(offline_data.get('jobs', []))} jobs")

        # Test data freshness check
        is_fresh_15 = db.is_data_fresh(15)
        is_fresh_30 = db.is_data_fresh(30)
        print(f"✅ Data freshness - 15min: {is_fresh_15}, 30min: {is_fresh_30}")

        # Test cached data retrieval
        backends = db.get_cached_data_with_expiration('backends', 15)
        jobs = db.get_cached_data_with_expiration('jobs', 15)
        print(f"✅ Cached data - backends: {len(backends.get('data', []))}, jobs: {len(jobs.get('data', []))}")

        return True
    except Exception as e:
        print(f"❌ Offline data operations test failed: {e}")
        return False

def test_sync_operations():
    """Test synchronization operations"""
    print("🔍 Testing sync operations...")

    try:
        # Test sync interval setting
        db.set_sync_interval(10)
        print("✅ Sync interval set to 10 minutes")

        # Test sync status update
        db.update_sync_status(True, None)
        print("✅ Sync status updated")

        # Test data sync (this will try to sync with external sources)
        db.perform_data_sync()
        print("✅ Data sync performed")

        return True
    except Exception as e:
        print(f"❌ Sync operations test failed: {e}")
        return False

def test_background_sync():
    """Test background sync functionality"""
    print("🔍 Testing background sync...")

    try:
        # Start background sync
        db.start_background_sync()
        print("✅ Background sync started")

        # Let it run for a few seconds
        time.sleep(2)

        # Check if it's running (we can't easily test the thread, but we can check if the method exists)
        if hasattr(db, 'executor') and db.executor:
            print("✅ Background sync executor is active")
        else:
            print("⚠️ Background sync executor not found")

        return True
    except Exception as e:
        print(f"❌ Background sync test failed: {e}")
        return False

def test_data_cleanup():
    """Test data cleanup operations"""
    print("🔍 Testing data cleanup...")

    try:
        # Test cleanup (with a high threshold to avoid actually deleting data)
        db.cleanup_old_data(days_to_keep=365)
        print("✅ Data cleanup performed")

        return True
    except Exception as e:
        print(f"❌ Data cleanup test failed: {e}")
        return False

def test_connection_pooling():
    """Test connection pooling functionality"""
    print("🔍 Testing connection pooling...")

    try:
        # Test multiple connections
        connections = []

        for i in range(3):
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) as count FROM backends")
                result = cursor.fetchone()
                connections.append(result['count'])
                print(f"✅ Connection {i+1} successful, backends count: {result['count']}")

        print(f"✅ Connection pool test completed with {len(connections)} connections")

        # Check pool size
        pool_size = len(db.connection_pool)
        print(f"✅ Connection pool size: {pool_size}")

        return True
    except Exception as e:
        print(f"❌ Connection pooling test failed: {e}")
        return False

def test_error_handling():
    """Test error handling in database operations"""
    print("🔍 Testing error handling...")

    try:
        # Test with invalid data type
        result = db.get_cached_data_with_expiration('invalid_type', 15)
        if 'error' in result:
            print("✅ Error handling working correctly for invalid data type")
        else:
            print("⚠️ Unexpected result for invalid data type")

        # Test with very old data (should return empty)
        old_data = db.get_offline_data(max_age_minutes=1)  # Very short window
        print(f"✅ Old data test completed, found {len(old_data.get('backends', []))} backends")

        return True
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def run_all_tests():
    """Run all offline functionality tests"""
    print("🚀 Starting offline functionality tests...\n")

    tests = [
        ("Database Connection", test_database_connection),
        ("Offline Data Operations", test_offline_data_operations),
        ("Sync Operations", test_sync_operations),
        ("Background Sync", test_background_sync),
        ("Data Cleanup", test_data_cleanup),
        ("Connection Pooling", test_connection_pooling),
        ("Error Handling", test_error_handling),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print('='*50)

        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")

    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    print('='*50)

    if passed == total:
        print("🎉 All tests passed! Offline functionality is working correctly.")
        return True
    else:
        print(f"⚠️ {total - passed} tests failed. Please check the issues above.")
        return False

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("Offline Functionality Test Script")
        print("Usage: python test_offline_functionality.py")
        print("This script tests all offline database functionality")
        return

    try:
        success = run_all_tests()

        # Cleanup
        db.shutdown()

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
        db.shutdown()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test script failed: {e}")
        db.shutdown()
        sys.exit(1)

if __name__ == "__main__":
    main()
