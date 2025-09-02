from http.server import BaseHTTPRequestHandler
import json
import random

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Generar status del sistema
        status_data = {
            'status': 'online',
            'uptime': random.randint(1000, 9999),
            'total_signals': random.randint(150, 300),
            'technical_signals': random.randint(80, 150),
            'historical_signals': random.randint(40, 80),
            'fundamental_signals': random.randint(30, 70),
            'last_update': '2025-09-02T14:00:00Z',
            'version': '1.0.0'
        }
        
        self.wfile.write(json.dumps(status_data).encode())
        return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
