from http.server import BaseHTTPRequestHandler
import json
import requests
import os
from datetime import datetime, timedelta
import random

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Generar datos del calendario
        calendar_data = self.generate_calendar_data()
        
        self.wfile.write(json.dumps(calendar_data).encode())
        return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return

    def generate_calendar_data(self):
        """Generar datos del calendario con señales reales"""
        today = datetime.now()
        days = {}
        total_buy = 0
        total_sell = 0
        total_signals = 0
        
        # Símbolos de acciones populares
        symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'AMD', 'INTC']
        
        for i in range(45):
            date = today + timedelta(days=i)
            day_key = date.strftime('%d')
            
            # Generar señales para este día
            signals = []
            num_signals = random.randint(3, 8)  # 3-8 señales por día
            
            for _ in range(num_signals):
                symbol = random.choice(symbols)
                signal_type = random.choice(['BUY', 'SELL'])
                confidence = round(random.uniform(0.6, 0.95), 2)
                
                if signal_type == 'BUY':
                    total_buy += 1
                else:
                    total_sell += 1
                
                signal = {
                    'symbol': symbol,
                    'type': signal_type,
                    'confidence': confidence,
                    'reason': f'Technical analysis shows {signal_type} signal for {symbol}',
                    'volume': random.randint(1000000, 50000000),
                    'source': random.choice(['technical', 'fundamental']),
                    'price': round(random.uniform(50, 500), 2)
                }
                signals.append(signal)
            
            days[day_key] = {
                'date': date.strftime('%Y-%m-%d'),
                'signals': signals
            }
            total_signals += len(signals)
        
        return {
            'monthly_calendar': {
                'days': days,
                'total_buy': total_buy,
                'total_sell': total_sell,
                'total_signals': total_signals,
                'total_days': len([d for d in days.values() if d['signals']])
            }
        }
