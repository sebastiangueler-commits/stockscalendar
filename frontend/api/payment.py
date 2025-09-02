from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Planes de pago
        plans_data = {
            'success': True,
            'plans': [
                {
                    'id': 'monthly',
                    'name': 'Monthly Plan',
                    'price': '9.99',
                    'period': 'month',
                    'features': [
                        'Full access to all signals',
                        'Real-time technical signals',
                        'Historical signals (last 2 years)',
                        'Fundamental signals (P/E, P/B, ROE)',
                        '45-day calendar forecast',
                        'Email alerts',
                        'Technical support',
                        'Premium features included'
                    ]
                },
                {
                    'id': 'yearly',
                    'name': 'Annual Plan',
                    'price': '99.99',
                    'period': 'year',
                    'features': [
                        'Full access to all signals',
                        'Real-time technical signals',
                        'Historical signals (last 5 years)',
                        'Advanced fundamental signals',
                        '45-day calendar forecast',
                        'Email and SMS alerts',
                        'Priority support',
                        'Custom portfolio analysis',
                        'Save 17% vs monthly'
                    ]
                },
                {
                    'id': 'lifetime',
                    'name': 'Lifetime Plan',
                    'price': '300.00',
                    'period': 'lifetime',
                    'features': [
                        'Full access to all signals',
                        'Real-time technical signals',
                        'Complete historical signals',
                        'Premium fundamental signals',
                        '45-day calendar forecast',
                        'Email, SMS and WhatsApp alerts',
                        'VIP 24/7 support',
                        'Advanced portfolio analysis',
                        'Access to new features',
                        'No renewals needed',
                        'Best value - One payment forever'
                    ]
                }
            ]
        }
        
        self.wfile.write(json.dumps(plans_data).encode())
        return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
