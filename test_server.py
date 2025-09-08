#!/usr/bin/env python3
"""
Test server startup
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

try:
    print("🔄 Importing app...")
    import app
    print("✅ App imported successfully")
    
    print("🔄 Initializing database...")
    app.init_database()
    print("✅ Database initialized")
    
    print("🔄 Starting server...")
    print("Server should be running on http://localhost:5003")
    print("Press Ctrl+C to stop")
    
    # Start the server
    app.app.run(host='127.0.0.1', port=5003, debug=True)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
