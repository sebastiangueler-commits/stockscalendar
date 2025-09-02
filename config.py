#!/usr/bin/env python3
"""
Configuración para APIs reales de datos de acciones
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# APIs para datos reales de acciones
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
IEX_CLOUD_API_KEY = os.getenv("IEX_CLOUD_API_KEY", "Tpk_018b97bce0a24c0d9c632c01c3c7c5c8")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "demo")

# PayPal Configuration
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "demo")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET", "demo")
PAYPAL_MODE = os.getenv("PAYPAL_MODE", "sandbox")

# Configuración de la aplicación
APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# URLs de APIs
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
IEX_CLOUD_BASE_URL = "https://cloud.iexapis.com/stable"
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

# Configuración de cache
CACHE_DURATION_MINUTES = 5
RATE_LIMIT_DELAY_SECONDS = 0.5

# Lista de acciones reales (S&P 500 + NASDAQ 100 + acciones importantes)
REAL_STOCKS = [
    # Tech Giants
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'ADBE', 'CRM',
    'AMD', 'INTC', 'CSCO', 'ORCL', 'QCOM', 'AVGO', 'TXN', 'MU', 'ADI', 'KLAC',
    'CDNS', 'MRVL', 'WDAY', 'ZM', 'TEAM', 'OKTA', 'CRWD', 'ZS', 'PLTR', 'SNOW',
    'DDOG', 'NET', 'SQ', 'ROKU', 'SHOP', 'SPOT', 'PINS', 'SNAP', 'UBER', 'LYFT',
    'DASH', 'ABNB', 'COIN', 'HOOD', 'RBLX', 'TTD', 'DOCU', 'TWLO', 'ESTC', 'MDB',
    
    # Financial Services
    'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'USB', 'PNC', 'TFC', 'COF',
    'AXP', 'V', 'MA', 'DIS', 'KO', 'PEP', 'PG', 'JNJ', 'PFE', 'MRK',
    'ABBV', 'LLY', 'UNH', 'CVS', 'CI', 'HUM', 'WMT', 'HD', 'LOW', 'COST',
    'TGT', 'CVX', 'XOM', 'COP', 'EOG', 'SLB', 'HAL', 'BKR', 'GE', 'BA',
    'CAT', 'DE', 'MMM', 'HON', 'UPS', 'FDX', 'RTX', 'LMT', 'NOC', 'GD',
    
    # Healthcare & Biotech
    'JNJ', 'PFE', 'MRK', 'ABBV', 'LLY', 'UNH', 'CVS', 'CI', 'HUM', 'TMO',
    'ABT', 'DHR', 'BMY', 'GILD', 'AMGN', 'BIIB', 'REGN', 'VRTX', 'MRNA', 'BNTX',
    
    # Energy & Materials
    'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'HAL', 'BKR', 'XLE', 'USO', 'UNG',
    'FCX', 'NEM', 'AA', 'LIN', 'APD', 'NEE', 'DUK', 'SO', 'D', 'AEP',
    
    # Consumer & Retail
    'WMT', 'TGT', 'COST', 'HD', 'LOW', 'MCD', 'SBUX', 'YUM', 'NKE', 'UA',
    'LULU', 'TJX', 'ROST', 'BURL', 'ULTA', 'SIG', 'BBY', 'GME', 'AMC', 'BBBY',
    
    # Real Estate & Utilities
    'SPG', 'PLD', 'EQIX', 'AMT', 'CCI', 'DLR', 'O', 'WELL', 'VICI', 'PSA',
    'NEE', 'DUK', 'SO', 'D', 'AEP', 'XEL', 'ED', 'EIX', 'PEG', 'WEC',
    
    # Acciones especiales incluyendo MEIP
    'MEIP', 'GME', 'AMC', 'BBBY', 'NOK', 'BB', 'SNDL', 'HEXO', 'ACB', 'TLRY',
    'CGC', 'APHA', 'CRON', 'OGI', 'VFF', 'KERN', 'JBLU', 'SAVE', 'UAL', 'DAL',
    'AAL', 'LUV', 'HA', 'ALK', 'JETS', 'XLE', 'USO', 'UNG', 'GLD', 'SLV',
    'GDX', 'GDXJ', 'BTC', 'ETH', 'ADA', 'DOT', 'LINK', 'UNI', 'LTC', 'BCH',
    'XRP', 'DOGE', 'SHIB', 'MATIC', 'AVAX', 'SOL', 'ATOM', 'FTT', 'LUNA', 'UST'
]

# Configuración de análisis
ANALYSIS_BATCH_SIZE = 20
ANALYSIS_DELAY_SECONDS = 0.5
BATCH_DELAY_SECONDS = 2

# Configuración de señales
MIN_SIGNALS_PER_DAY = 2
MAX_SIGNALS_PER_DAY = 6
FORECAST_DAYS = 45

# Configuración de confianza
MIN_CONFIDENCE = 0.1
MAX_CONFIDENCE = 0.95
BUY_THRESHOLD = 0.6
SELL_THRESHOLD = 0.4
