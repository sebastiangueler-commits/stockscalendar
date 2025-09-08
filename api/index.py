from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Database setup
DB_PATH = 'database.db'

def init_database():
    """Initialize the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                subscription_type TEXT DEFAULT 'free',
                is_admin BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Signals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                analysis_type TEXT NOT NULL,
                price REAL,
                change_percent REAL,
                recommendation TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create admin user
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO users (username, password, email, subscription_type, is_admin)
                VALUES (?, ?, ?, ?, ?)
            ''', ('admin', 'admin123', 'admin@stockscalendar.com', 'forever', True))
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")
        
    except Exception as e:
        print(f"❌ Database error: {e}")

# Initialize database
init_database()

@app.route('/')
def home():
    return jsonify({
        'message': 'Stocks Calendar API',
        'status': 'running',
        'version': '1.0.0'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Server is running'
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
            
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, subscription_type, is_admin
            FROM users
            WHERE username = ? AND password = ?
        ''', (username, password))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return jsonify({
                'success': True,
                'user': {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'subscription_type': user[3],
                    'is_admin': bool(user[4])
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Login error: {str(e)}'}), 500

@app.route('/api/signals')
def get_signals():
    """Get all signals"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT symbol, signal_type, analysis_type, price, change_percent, 
                   recommendation, created_at
            FROM signals
            ORDER BY created_at DESC
        ''')
        
        signals = []
        for row in cursor.fetchall():
            signals.append({
                'symbol': row[0],
                'signal_type': row[1],
                'analysis_type': row[2],
                'price': row[3],
                'change_percent': row[4],
                'recommendation': row[5],
                'created_at': row[6]
            })
        
        conn.close()
        return jsonify(signals)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get basic stats"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM signals')
        total_signals = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_signals': total_signals,
            'total_users': total_users,
            'buy_fundamental': 0,
            'buy_technical': 0,
            'sell_fundamental': 0,
            'sell_technical': 0
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# For Vercel
handler = app

if __name__ == '__main__':
    app.run(debug=True)