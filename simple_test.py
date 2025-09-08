#!/usr/bin/env python3
"""
Simple test to verify login logic
"""
import sqlite3

def test_login_logic():
    """Test the login logic directly"""
    DB_PATH = 'database.db'
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Test the exact query from the login function
        cursor.execute('''
            SELECT id, username, email, subscription_type, is_admin
            FROM users
            WHERE username = ? AND password = ?
        ''', ('admin', 'admin123'))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            print("✅ Login logic works correctly!")
            print(f"User data: {user}")
            return True
        else:
            print("❌ Login logic failed - user not found")
            return False
            
    except Exception as e:
        print(f"❌ Error in login logic: {e}")
        return False

if __name__ == "__main__":
    test_login_logic()
