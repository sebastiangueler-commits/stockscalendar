#!/usr/bin/env python3
"""
Test script to verify login functionality
"""
import requests
import json

def test_login():
    """Test the login endpoint"""
    url = "http://localhost:5003/api/auth/login"
    data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        print("🧪 Testing login with admin credentials...")
        response = requests.post(url, json=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Login successful: {result}")
        else:
            print(f"❌ Login failed: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the app is running on localhost:5003")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login()
