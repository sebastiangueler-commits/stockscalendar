#!/usr/bin/env python3
"""
Test login with alternative port
"""
import requests
import json

def test_login_alt():
    """Test the login endpoint on alternative port"""
    url = "http://localhost:8000/api/auth/login"
    data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        print("🧪 Testing login on port 8000...")
        response = requests.post(url, json=data)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Login successful: {result}")
        else:
            print(f"❌ Login failed: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server on port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login_alt()
