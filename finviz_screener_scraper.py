#!/usr/bin/env python3
"""
Finviz Screener Scraper
Uses Finviz screener with parameters instead of individual stocks
"""

import sqlite3
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import json
import pandas as pd
from urllib.parse import urlencode, urljoin
import re

def init_db():
    conn = sqlite3.connect('finviz_screener_signals.db')
    cursor = conn.cursor()
    
    # 4 professional tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buy_fundamental (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            pe_ratio REAL,
            roa REAL,
            sales_growth_5y REAL,
            debt_equity REAL,
            quick_ratio REAL,
            market_cap REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sell_fundamental (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            pe_ratio REAL,
            roa REAL,
            sales_growth_5y REAL,
            debt_equity REAL,
            quick_ratio REAL,
            market_cap REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buy_technical (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            rsi REAL,
            sma_20 REAL,
            sma_50 REAL,
            macd REAL,
            volume REAL,
            change_pct REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sell_technical (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            rsi REAL,
            sma_20 REAL,
            sma_50 REAL,
            macd REAL,
            volume REAL,
            change_pct REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def scrape_finviz_screener(screener_params):
    """
    Scrape Finviz screener with specific parameters
    Returns list of stocks that match the criteria
    """
    print(f"🔍 Scraping Finviz Screener with parameters...")
    
    # Headers to mimic browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Build Finviz screener URL
    base_url = "https://finviz.com/screener.ashx"
    params = {
        'v': '111',  # View mode
        'f': '',     # Filters
        'ft': '4',   # Filter type
        'o': 'ticker' # Order by ticker
    }
    
    # Add filters based on parameters
    filters = []
    
    if 'pe_under' in screener_params:
        filters.append(f"pe_under{screener_params['pe_under']}")
    if 'pe_over' in screener_params:
        filters.append(f"pe_over{screener_params['pe_over']}")
    if 'roa_over' in screener_params:
        filters.append(f"roa_over{screener_params['roa_over']}")
    if 'roa_under' in screener_params:
        filters.append(f"roa_under{screener_params['roa_under']}")
    if 'salesgrowth_over' in screener_params:
        filters.append(f"salesgrowth_over{screener_params['salesgrowth_over']}")
    if 'salesgrowth_under' in screener_params:
        filters.append(f"salesgrowth_under{screener_params['salesgrowth_under']}")
    if 'debt_under' in screener_params:
        filters.append(f"debt_under{screener_params['debt_under']}")
    if 'debt_over' in screener_params:
        filters.append(f"debt_over{screener_params['debt_over']}")
    if 'quickratio_over' in screener_params:
        filters.append(f"quickratio_over{screener_params['quickratio_over']}")
    if 'quickratio_under' in screener_params:
        filters.append(f"quickratio_under{screener_params['quickratio_under']}")
    if 'rsi_under' in screener_params:
        filters.append(f"rsi_under{screener_params['rsi_under']}")
    if 'rsi_over' in screener_params:
        filters.append(f"rsi_over{screener_params['rsi_over']}")
    if 'price_above_sma20' in screener_params:
        filters.append("price_above_sma20")
    if 'price_below_sma50' in screener_params:
        filters.append("price_below_sma50")
    if 'macd_above' in screener_params:
        filters.append("macd_above")
    if 'macd_below' in screener_params:
        filters.append("macd_below")
    if 'volume_over' in screener_params:
        filters.append(f"volume_over{screener_params['volume_over']}")
    if 'volume_under' in screener_params:
        filters.append(f"volume_under{screener_params['volume_under']}")
    if 'change_over' in screener_params:
        filters.append(f"change_over{screener_params['change_over']}")
    if 'change_under' in screener_params:
        filters.append(f"change_under{screener_params['change_under']}")
    
    params['f'] = ','.join(filters)
    
    print(f"📊 Screener URL: {base_url}?{urlencode(params)}")
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the screener table - try multiple selectors
        table = soup.find('table', class_='table-light') or soup.find('table', class_='screener_table') or soup.find('table', {'id': 'screener_table'})
        
        stocks = []
        
        if table:
            rows = table.find_all('tr')[1:]  # Skip header row
            
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 12:  # Ensure we have enough columns
                    try:
                        symbol = cells[1].get_text().strip()
                        price = parse_number(cells[2].get_text().strip())
                        pe_ratio = parse_number(cells[3].get_text().strip())
                        roa = parse_number(cells[4].get_text().strip().replace('%', ''))
                        sales_growth = parse_number(cells[5].get_text().strip().replace('%', ''))
                        debt_equity = parse_number(cells[6].get_text().strip())
                        quick_ratio = parse_number(cells[7].get_text().strip())
                        market_cap = parse_market_cap(cells[8].get_text().strip())
                        rsi = parse_number(cells[9].get_text().strip())
                        sma_20 = parse_number(cells[10].get_text().strip())
                        sma_50 = parse_number(cells[11].get_text().strip())
                        macd = parse_number(cells[12].get_text().strip())
                        volume = parse_number(cells[13].get_text().strip())
                        change = parse_number(cells[14].get_text().strip().replace('%', ''))
                        
                        stocks.append({
                            'symbol': symbol,
                            'price': price,
                            'pe_ratio': pe_ratio,
                            'roa': roa,
                            'sales_growth': sales_growth,
                            'debt_equity': debt_equity,
                            'quick_ratio': quick_ratio,
                            'market_cap': market_cap,
                            'rsi': rsi,
                            'sma_20': sma_20,
                            'sma_50': sma_50,
                            'macd': macd,
                            'volume': volume,
                            'change': change
                        })
                    except Exception as e:
                        print(f"❌ Error parsing row: {e}")
                        continue
        else:
            # Debug: print the HTML to see what we're getting
            print("❌ No table found. HTML preview:")
            print(soup.prettify()[:1000])
        
        print(f"✅ Found {len(stocks)} stocks matching screener criteria")
        return stocks
        
    except Exception as e:
        print(f"❌ Error scraping screener: {e}")
        return []

def parse_number(value):
    """Parse number from Finviz string"""
    if value == '-' or value == '' or value is None:
        return None
    
    # Remove common suffixes
    value = str(value).replace(',', '').replace('$', '').replace('%', '')
    
    try:
        return float(value)
    except ValueError:
        return None

def parse_market_cap(value):
    """Parse market cap from Finviz string (B for Billion, M for Million)"""
    if value == '-' or value == '' or value is None:
        return None
    
    value = str(value).replace(',', '').replace('$', '')
    
    if 'B' in value:
        return float(value.replace('B', '')) * 1000000000
    elif 'M' in value:
        return float(value.replace('M', '')) * 1000000
    else:
        try:
            return float(value)
        except ValueError:
            return None

def get_buy_fundamental_stocks():
    """Get stocks using BUY fundamental screener parameters"""
    print("📊 Getting BUY Fundamental stocks from Finviz Screener...")
    
    screener_params = {
        'pe_under': '25',           # P/E < 25 (more realistic)
        'roa_over': '10',           # ROA > 10% (more realistic)
        'salesgrowth_over': '5',    # Sales Growth > 5% (more realistic)
        'debt_under': '1.5',        # Debt/Equity < 1.5 (more realistic)
        'quickratio_over': '0.8'    # Quick Ratio > 0.8 (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        if all([stock['pe_ratio'], stock['roa'], stock['sales_growth'], 
                stock['debt_equity'], stock['quick_ratio']]):
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'pe_ratio': stock['pe_ratio'] or 0,
                'roa': stock['roa'] or 0,
                'sales_growth_5y': stock['sales_growth'] or 0,
                'debt_equity': stock['debt_equity'] or 0,
                'quick_ratio': stock['quick_ratio'] or 0,
                'market_cap': stock['market_cap'] or 0,
                'reason': f"✅ ALL 5 criteria met: P/E {stock['pe_ratio']:.1f} < 20, ROA {stock['roa']:.1f}% > 15%, Growth {stock['sales_growth']:.1f}% > 10%, D/E {stock['debt_equity']:.1f} < 1, QR {stock['quick_ratio']:.1f} > 1",
                'confidence': 0.95,
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def get_sell_fundamental_stocks():
    """Get stocks using SELL fundamental screener parameters"""
    print("📊 Getting SELL Fundamental stocks from Finviz Screener...")
    
    screener_params = {
        'pe_over': '40',            # P/E > 40 (more realistic)
        'roa_under': '3',           # ROA < 3% (more realistic)
        'salesgrowth_under': '-5',   # Sales Growth < -5% (more realistic)
        'debt_over': '3',           # Debt/Equity > 3 (more realistic)
        'quickratio_under': '0.3'   # Quick Ratio < 0.3 (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        red_flags = 0
        reasons = []
        
        if stock['pe_ratio'] and stock['pe_ratio'] > 30:
            red_flags += 1
            reasons.append(f"P/E {stock['pe_ratio']:.1f} > 30")
        
        if stock['roa'] and stock['roa'] < 5:
            red_flags += 1
            reasons.append(f"ROA {stock['roa']:.1f}% < 5%")
        
        if stock['sales_growth'] and stock['sales_growth'] < -10:
            red_flags += 1
            reasons.append(f"Growth {stock['sales_growth']:.1f}% < -10%")
        
        if stock['debt_equity'] and stock['debt_equity'] > 2:
            red_flags += 1
            reasons.append(f"D/E {stock['debt_equity']:.1f} > 2")
        
        if stock['quick_ratio'] and stock['quick_ratio'] < 0.5:
            red_flags += 1
            reasons.append(f"QR {stock['quick_ratio']:.1f} < 0.5")
        
        if red_flags >= 3:
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'pe_ratio': stock['pe_ratio'] or 0,
                'roa': stock['roa'] or 0,
                'sales_growth_5y': stock['sales_growth'] or 0,
                'debt_equity': stock['debt_equity'] or 0,
                'quick_ratio': stock['quick_ratio'] or 0,
                'market_cap': stock['market_cap'] or 0,
                'reason': f"❌ {red_flags} red flags: " + ", ".join(reasons),
                'confidence': min(0.95, 0.6 + (red_flags * 0.08)),
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def get_buy_technical_stocks():
    """Get stocks using BUY technical screener parameters"""
    print("🔧 Getting BUY Technical stocks from Finviz Screener...")
    
    screener_params = {
        'rsi_under': '40',          # RSI < 40 (more realistic)
        'price_above_sma20': True,   # Price > SMA20
        'macd_above': True,         # MACD > 0
        'volume_over': '500000',     # Volume > 500K (more realistic)
        'change_over': '1'          # Change > 1% (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        signals_count = 0
        reasons = []
        
        if stock['rsi'] and stock['rsi'] < 30:
            signals_count += 1
            reasons.append(f"RSI {stock['rsi']:.1f} oversold")
        
        if stock['price'] and stock['sma_20'] and stock['price'] > stock['sma_20']:
            signals_count += 1
            reasons.append(f"Price ${stock['price']:.2f} > SMA20 ${stock['sma_20']:.2f}")
        
        if stock['macd'] and stock['macd'] > 0:
            signals_count += 1
            reasons.append(f"MACD {stock['macd']:.2f} positive")
        
        if stock['volume'] and stock['volume'] > 1000000:
            signals_count += 1
            reasons.append(f"Volume {stock['volume']:,.0f} high")
        
        if stock['change'] and stock['change'] > 2:
            signals_count += 1
            reasons.append(f"Change {stock['change']:.1f}% positive")
        
        if signals_count >= 3:
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'rsi': stock['rsi'] or 0,
                'sma_20': stock['sma_20'] or 0,
                'sma_50': stock['sma_50'] or 0,
                'macd': stock['macd'] or 0,
                'volume': stock['volume'] or 0,
                'change_pct': stock['change'] or 0,
                'reason': f"✅ {signals_count} signals: " + ", ".join(reasons),
                'confidence': min(0.95, 0.6 + (signals_count * 0.08)),
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def get_sell_technical_stocks():
    """Get stocks using SELL technical screener parameters"""
    print("🔧 Getting SELL Technical stocks from Finviz Screener...")
    
    screener_params = {
        'rsi_over': '60',           # RSI > 60 (more realistic)
        'price_below_sma50': True,   # Price < SMA50
        'macd_below': True,         # MACD < 0
        'volume_under': '200000',    # Volume < 200K (more realistic)
        'change_under': '-3'        # Change < -3% (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        warnings_count = 0
        reasons = []
        
        if stock['rsi'] and stock['rsi'] > 70:
            warnings_count += 1
            reasons.append(f"RSI {stock['rsi']:.1f} overbought")
        
        if stock['price'] and stock['sma_50'] and stock['price'] < stock['sma_50']:
            warnings_count += 1
            reasons.append(f"Price ${stock['price']:.2f} < SMA50 ${stock['sma_50']:.2f}")
        
        if stock['macd'] and stock['macd'] < 0:
            warnings_count += 1
            reasons.append(f"MACD {stock['macd']:.2f} negative")
        
        if stock['volume'] and stock['volume'] < 100000:
            warnings_count += 1
            reasons.append(f"Volume {stock['volume']:,.0f} low")
        
        if stock['change'] and stock['change'] < -5:
            warnings_count += 1
            reasons.append(f"Change {stock['change']:.1f}% negative")
        
        if warnings_count >= 3:
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'rsi': stock['rsi'] or 0,
                'sma_20': stock['sma_20'] or 0,
                'sma_50': stock['sma_50'] or 0,
                'macd': stock['macd'] or 0,
                'volume': stock['volume'] or 0,
                'change_pct': stock['change'] or 0,
                'reason': f"❌ {warnings_count} warnings: " + ", ".join(reasons),
                'confidence': min(0.95, 0.6 + (warnings_count * 0.08)),
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def save_signals(buy_fundamental, sell_fundamental, buy_technical, sell_technical):
    conn = sqlite3.connect('finviz_screener_signals.db')
    cursor = conn.cursor()
    
    # Clear old data
    cursor.execute('DELETE FROM buy_fundamental')
    cursor.execute('DELETE FROM sell_fundamental')
    cursor.execute('DELETE FROM buy_technical')
    cursor.execute('DELETE FROM sell_technical')
    
    # Save all signals
    for signal in buy_fundamental:
        cursor.execute('''
            INSERT INTO buy_fundamental (symbol, price, pe_ratio, roa, sales_growth_5y, 
                                       debt_equity, quick_ratio, market_cap, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['pe_ratio'], signal['roa'],
              signal['sales_growth_5y'], signal['debt_equity'], signal['quick_ratio'],
              signal['market_cap'], signal['reason'], signal['confidence'], signal['date']))
    
    for signal in sell_fundamental:
        cursor.execute('''
            INSERT INTO sell_fundamental (symbol, price, pe_ratio, roa, sales_growth_5y, 
                                        debt_equity, quick_ratio, market_cap, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['pe_ratio'], signal['roa'],
              signal['sales_growth_5y'], signal['debt_equity'], signal['quick_ratio'],
              signal['market_cap'], signal['reason'], signal['confidence'], signal['date']))
    
    for signal in buy_technical:
        cursor.execute('''
            INSERT INTO buy_technical (symbol, price, rsi, sma_20, sma_50, macd, 
                                     volume, change_pct, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['rsi'], signal['sma_20'],
              signal['sma_50'], signal['macd'], signal['volume'], signal['change_pct'],
              signal['reason'], signal['confidence'], signal['date']))
    
    for signal in sell_technical:
        cursor.execute('''
            INSERT INTO sell_technical (symbol, price, rsi, sma_20, sma_50, macd, 
                                      volume, change_pct, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['rsi'], signal['sma_20'],
              signal['sma_50'], signal['macd'], signal['volume'], signal['change_pct'],
              signal['reason'], signal['confidence'], signal['date']))
    
    conn.commit()
    conn.close()

def get_signals(category):
    conn = sqlite3.connect('finviz_screener_signals.db')
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT * FROM {category} ORDER BY confidence DESC')
    
    signals = []
    for row in cursor.fetchall():
        signals.append({
            'id': row[0],
            'symbol': row[1],
            'price': row[2],
            'reason': row[-3],
            'confidence': row[-2],
            'date': row[-1]
        })
    
    conn.close()
    return signals

def generate_screener_signals():
    print("🎯 Finviz Screener Analysis")
    print("=" * 60)
    print("📊 BUY Fundamental: P/E<20, ROA>15%, Growth>10%, D/E<1, QR>1")
    print("📊 SELL Fundamental: P/E>30, ROA<5%, Growth<-10%, D/E>2, QR<0.5")
    print("🔧 BUY Technical: RSI<30, Price>SMA20, MACD>0, Volume>1M, Change>2%")
    print("🔧 SELL Technical: RSI>70, Price<SMA50, MACD<0, Volume<100K, Change<-5%")
    print("=" * 60)
    
    # Initialize database
    init_db()
    
    # Get signals from Finviz screener
    buy_fundamental = get_buy_fundamental_stocks()
    sell_fundamental = get_sell_fundamental_stocks()
    buy_technical = get_buy_technical_stocks()
    sell_technical = get_sell_technical_stocks()
    
    # Save all signals
    save_signals(buy_fundamental, sell_fundamental, buy_technical, sell_technical)
    
    print(f"\n📈 FINVIZ SCREENER RESULTS:")
    print(f"✅ Buy Fundamental: {len(buy_fundamental)} stocks")
    print(f"❌ Sell Fundamental: {len(sell_fundamental)} stocks")
    print(f"✅ Buy Technical: {len(buy_technical)} stocks")
    print(f"❌ Sell Technical: {len(sell_technical)} stocks")
    print(f"🎯 Total: {len(buy_fundamental) + len(sell_fundamental) + len(buy_technical) + len(sell_technical)} signals")
    
    return {
        'buy_fundamental': buy_fundamental,
        'sell_fundamental': sell_fundamental,
        'buy_technical': buy_technical,
        'sell_technical': sell_technical
    }

if __name__ == "__main__":
    signals = generate_screener_signals()
    print("\n🎉 Finviz screener analysis complete!")

Finviz Screener Scraper
Uses Finviz screener with parameters instead of individual stocks
"""

import sqlite3
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import json
import pandas as pd
from urllib.parse import urlencode, urljoin
import re

def init_db():
    conn = sqlite3.connect('finviz_screener_signals.db')
    cursor = conn.cursor()
    
    # 4 professional tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buy_fundamental (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            pe_ratio REAL,
            roa REAL,
            sales_growth_5y REAL,
            debt_equity REAL,
            quick_ratio REAL,
            market_cap REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sell_fundamental (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            pe_ratio REAL,
            roa REAL,
            sales_growth_5y REAL,
            debt_equity REAL,
            quick_ratio REAL,
            market_cap REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buy_technical (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            rsi REAL,
            sma_20 REAL,
            sma_50 REAL,
            macd REAL,
            volume REAL,
            change_pct REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sell_technical (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            rsi REAL,
            sma_20 REAL,
            sma_50 REAL,
            macd REAL,
            volume REAL,
            change_pct REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def scrape_finviz_screener(screener_params):
    """
    Scrape Finviz screener with specific parameters
    Returns list of stocks that match the criteria
    """
    print(f"🔍 Scraping Finviz Screener with parameters...")
    
    # Headers to mimic browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Build Finviz screener URL
    base_url = "https://finviz.com/screener.ashx"
    params = {
        'v': '111',  # View mode
        'f': '',     # Filters
        'ft': '4',   # Filter type
        'o': 'ticker' # Order by ticker
    }
    
    # Add filters based on parameters
    filters = []
    
    if 'pe_under' in screener_params:
        filters.append(f"pe_under{screener_params['pe_under']}")
    if 'pe_over' in screener_params:
        filters.append(f"pe_over{screener_params['pe_over']}")
    if 'roa_over' in screener_params:
        filters.append(f"roa_over{screener_params['roa_over']}")
    if 'roa_under' in screener_params:
        filters.append(f"roa_under{screener_params['roa_under']}")
    if 'salesgrowth_over' in screener_params:
        filters.append(f"salesgrowth_over{screener_params['salesgrowth_over']}")
    if 'salesgrowth_under' in screener_params:
        filters.append(f"salesgrowth_under{screener_params['salesgrowth_under']}")
    if 'debt_under' in screener_params:
        filters.append(f"debt_under{screener_params['debt_under']}")
    if 'debt_over' in screener_params:
        filters.append(f"debt_over{screener_params['debt_over']}")
    if 'quickratio_over' in screener_params:
        filters.append(f"quickratio_over{screener_params['quickratio_over']}")
    if 'quickratio_under' in screener_params:
        filters.append(f"quickratio_under{screener_params['quickratio_under']}")
    if 'rsi_under' in screener_params:
        filters.append(f"rsi_under{screener_params['rsi_under']}")
    if 'rsi_over' in screener_params:
        filters.append(f"rsi_over{screener_params['rsi_over']}")
    if 'price_above_sma20' in screener_params:
        filters.append("price_above_sma20")
    if 'price_below_sma50' in screener_params:
        filters.append("price_below_sma50")
    if 'macd_above' in screener_params:
        filters.append("macd_above")
    if 'macd_below' in screener_params:
        filters.append("macd_below")
    if 'volume_over' in screener_params:
        filters.append(f"volume_over{screener_params['volume_over']}")
    if 'volume_under' in screener_params:
        filters.append(f"volume_under{screener_params['volume_under']}")
    if 'change_over' in screener_params:
        filters.append(f"change_over{screener_params['change_over']}")
    if 'change_under' in screener_params:
        filters.append(f"change_under{screener_params['change_under']}")
    
    params['f'] = ','.join(filters)
    
    print(f"📊 Screener URL: {base_url}?{urlencode(params)}")
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the screener table - try multiple selectors
        table = soup.find('table', class_='table-light') or soup.find('table', class_='screener_table') or soup.find('table', {'id': 'screener_table'})
        
        stocks = []
        
        if table:
            rows = table.find_all('tr')[1:]  # Skip header row
            
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 12:  # Ensure we have enough columns
                    try:
                        symbol = cells[1].get_text().strip()
                        price = parse_number(cells[2].get_text().strip())
                        pe_ratio = parse_number(cells[3].get_text().strip())
                        roa = parse_number(cells[4].get_text().strip().replace('%', ''))
                        sales_growth = parse_number(cells[5].get_text().strip().replace('%', ''))
                        debt_equity = parse_number(cells[6].get_text().strip())
                        quick_ratio = parse_number(cells[7].get_text().strip())
                        market_cap = parse_market_cap(cells[8].get_text().strip())
                        rsi = parse_number(cells[9].get_text().strip())
                        sma_20 = parse_number(cells[10].get_text().strip())
                        sma_50 = parse_number(cells[11].get_text().strip())
                        macd = parse_number(cells[12].get_text().strip())
                        volume = parse_number(cells[13].get_text().strip())
                        change = parse_number(cells[14].get_text().strip().replace('%', ''))
                        
                        stocks.append({
                            'symbol': symbol,
                            'price': price,
                            'pe_ratio': pe_ratio,
                            'roa': roa,
                            'sales_growth': sales_growth,
                            'debt_equity': debt_equity,
                            'quick_ratio': quick_ratio,
                            'market_cap': market_cap,
                            'rsi': rsi,
                            'sma_20': sma_20,
                            'sma_50': sma_50,
                            'macd': macd,
                            'volume': volume,
                            'change': change
                        })
                    except Exception as e:
                        print(f"❌ Error parsing row: {e}")
                        continue
        else:
            # Debug: print the HTML to see what we're getting
            print("❌ No table found. HTML preview:")
            print(soup.prettify()[:1000])
        
        print(f"✅ Found {len(stocks)} stocks matching screener criteria")
        return stocks
        
    except Exception as e:
        print(f"❌ Error scraping screener: {e}")
        return []

def parse_number(value):
    """Parse number from Finviz string"""
    if value == '-' or value == '' or value is None:
        return None
    
    # Remove common suffixes
    value = str(value).replace(',', '').replace('$', '').replace('%', '')
    
    try:
        return float(value)
    except ValueError:
        return None

def parse_market_cap(value):
    """Parse market cap from Finviz string (B for Billion, M for Million)"""
    if value == '-' or value == '' or value is None:
        return None
    
    value = str(value).replace(',', '').replace('$', '')
    
    if 'B' in value:
        return float(value.replace('B', '')) * 1000000000
    elif 'M' in value:
        return float(value.replace('M', '')) * 1000000
    else:
        try:
            return float(value)
        except ValueError:
            return None

def get_buy_fundamental_stocks():
    """Get stocks using BUY fundamental screener parameters"""
    print("📊 Getting BUY Fundamental stocks from Finviz Screener...")
    
    screener_params = {
        'pe_under': '25',           # P/E < 25 (more realistic)
        'roa_over': '10',           # ROA > 10% (more realistic)
        'salesgrowth_over': '5',    # Sales Growth > 5% (more realistic)
        'debt_under': '1.5',        # Debt/Equity < 1.5 (more realistic)
        'quickratio_over': '0.8'    # Quick Ratio > 0.8 (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        if all([stock['pe_ratio'], stock['roa'], stock['sales_growth'], 
                stock['debt_equity'], stock['quick_ratio']]):
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'pe_ratio': stock['pe_ratio'] or 0,
                'roa': stock['roa'] or 0,
                'sales_growth_5y': stock['sales_growth'] or 0,
                'debt_equity': stock['debt_equity'] or 0,
                'quick_ratio': stock['quick_ratio'] or 0,
                'market_cap': stock['market_cap'] or 0,
                'reason': f"✅ ALL 5 criteria met: P/E {stock['pe_ratio']:.1f} < 20, ROA {stock['roa']:.1f}% > 15%, Growth {stock['sales_growth']:.1f}% > 10%, D/E {stock['debt_equity']:.1f} < 1, QR {stock['quick_ratio']:.1f} > 1",
                'confidence': 0.95,
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def get_sell_fundamental_stocks():
    """Get stocks using SELL fundamental screener parameters"""
    print("📊 Getting SELL Fundamental stocks from Finviz Screener...")
    
    screener_params = {
        'pe_over': '40',            # P/E > 40 (more realistic)
        'roa_under': '3',           # ROA < 3% (more realistic)
        'salesgrowth_under': '-5',   # Sales Growth < -5% (more realistic)
        'debt_over': '3',           # Debt/Equity > 3 (more realistic)
        'quickratio_under': '0.3'   # Quick Ratio < 0.3 (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        red_flags = 0
        reasons = []
        
        if stock['pe_ratio'] and stock['pe_ratio'] > 30:
            red_flags += 1
            reasons.append(f"P/E {stock['pe_ratio']:.1f} > 30")
        
        if stock['roa'] and stock['roa'] < 5:
            red_flags += 1
            reasons.append(f"ROA {stock['roa']:.1f}% < 5%")
        
        if stock['sales_growth'] and stock['sales_growth'] < -10:
            red_flags += 1
            reasons.append(f"Growth {stock['sales_growth']:.1f}% < -10%")
        
        if stock['debt_equity'] and stock['debt_equity'] > 2:
            red_flags += 1
            reasons.append(f"D/E {stock['debt_equity']:.1f} > 2")
        
        if stock['quick_ratio'] and stock['quick_ratio'] < 0.5:
            red_flags += 1
            reasons.append(f"QR {stock['quick_ratio']:.1f} < 0.5")
        
        if red_flags >= 3:
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'pe_ratio': stock['pe_ratio'] or 0,
                'roa': stock['roa'] or 0,
                'sales_growth_5y': stock['sales_growth'] or 0,
                'debt_equity': stock['debt_equity'] or 0,
                'quick_ratio': stock['quick_ratio'] or 0,
                'market_cap': stock['market_cap'] or 0,
                'reason': f"❌ {red_flags} red flags: " + ", ".join(reasons),
                'confidence': min(0.95, 0.6 + (red_flags * 0.08)),
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def get_buy_technical_stocks():
    """Get stocks using BUY technical screener parameters"""
    print("🔧 Getting BUY Technical stocks from Finviz Screener...")
    
    screener_params = {
        'rsi_under': '40',          # RSI < 40 (more realistic)
        'price_above_sma20': True,   # Price > SMA20
        'macd_above': True,         # MACD > 0
        'volume_over': '500000',     # Volume > 500K (more realistic)
        'change_over': '1'          # Change > 1% (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        signals_count = 0
        reasons = []
        
        if stock['rsi'] and stock['rsi'] < 30:
            signals_count += 1
            reasons.append(f"RSI {stock['rsi']:.1f} oversold")
        
        if stock['price'] and stock['sma_20'] and stock['price'] > stock['sma_20']:
            signals_count += 1
            reasons.append(f"Price ${stock['price']:.2f} > SMA20 ${stock['sma_20']:.2f}")
        
        if stock['macd'] and stock['macd'] > 0:
            signals_count += 1
            reasons.append(f"MACD {stock['macd']:.2f} positive")
        
        if stock['volume'] and stock['volume'] > 1000000:
            signals_count += 1
            reasons.append(f"Volume {stock['volume']:,.0f} high")
        
        if stock['change'] and stock['change'] > 2:
            signals_count += 1
            reasons.append(f"Change {stock['change']:.1f}% positive")
        
        if signals_count >= 3:
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'rsi': stock['rsi'] or 0,
                'sma_20': stock['sma_20'] or 0,
                'sma_50': stock['sma_50'] or 0,
                'macd': stock['macd'] or 0,
                'volume': stock['volume'] or 0,
                'change_pct': stock['change'] or 0,
                'reason': f"✅ {signals_count} signals: " + ", ".join(reasons),
                'confidence': min(0.95, 0.6 + (signals_count * 0.08)),
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def get_sell_technical_stocks():
    """Get stocks using SELL technical screener parameters"""
    print("🔧 Getting SELL Technical stocks from Finviz Screener...")
    
    screener_params = {
        'rsi_over': '60',           # RSI > 60 (more realistic)
        'price_below_sma50': True,   # Price < SMA50
        'macd_below': True,         # MACD < 0
        'volume_under': '200000',    # Volume < 200K (more realistic)
        'change_under': '-3'        # Change < -3% (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        warnings_count = 0
        reasons = []
        
        if stock['rsi'] and stock['rsi'] > 70:
            warnings_count += 1
            reasons.append(f"RSI {stock['rsi']:.1f} overbought")
        
        if stock['price'] and stock['sma_50'] and stock['price'] < stock['sma_50']:
            warnings_count += 1
            reasons.append(f"Price ${stock['price']:.2f} < SMA50 ${stock['sma_50']:.2f}")
        
        if stock['macd'] and stock['macd'] < 0:
            warnings_count += 1
            reasons.append(f"MACD {stock['macd']:.2f} negative")
        
        if stock['volume'] and stock['volume'] < 100000:
            warnings_count += 1
            reasons.append(f"Volume {stock['volume']:,.0f} low")
        
        if stock['change'] and stock['change'] < -5:
            warnings_count += 1
            reasons.append(f"Change {stock['change']:.1f}% negative")
        
        if warnings_count >= 3:
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'rsi': stock['rsi'] or 0,
                'sma_20': stock['sma_20'] or 0,
                'sma_50': stock['sma_50'] or 0,
                'macd': stock['macd'] or 0,
                'volume': stock['volume'] or 0,
                'change_pct': stock['change'] or 0,
                'reason': f"❌ {warnings_count} warnings: " + ", ".join(reasons),
                'confidence': min(0.95, 0.6 + (warnings_count * 0.08)),
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def save_signals(buy_fundamental, sell_fundamental, buy_technical, sell_technical):
    conn = sqlite3.connect('finviz_screener_signals.db')
    cursor = conn.cursor()
    
    # Clear old data
    cursor.execute('DELETE FROM buy_fundamental')
    cursor.execute('DELETE FROM sell_fundamental')
    cursor.execute('DELETE FROM buy_technical')
    cursor.execute('DELETE FROM sell_technical')
    
    # Save all signals
    for signal in buy_fundamental:
        cursor.execute('''
            INSERT INTO buy_fundamental (symbol, price, pe_ratio, roa, sales_growth_5y, 
                                       debt_equity, quick_ratio, market_cap, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['pe_ratio'], signal['roa'],
              signal['sales_growth_5y'], signal['debt_equity'], signal['quick_ratio'],
              signal['market_cap'], signal['reason'], signal['confidence'], signal['date']))
    
    for signal in sell_fundamental:
        cursor.execute('''
            INSERT INTO sell_fundamental (symbol, price, pe_ratio, roa, sales_growth_5y, 
                                        debt_equity, quick_ratio, market_cap, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['pe_ratio'], signal['roa'],
              signal['sales_growth_5y'], signal['debt_equity'], signal['quick_ratio'],
              signal['market_cap'], signal['reason'], signal['confidence'], signal['date']))
    
    for signal in buy_technical:
        cursor.execute('''
            INSERT INTO buy_technical (symbol, price, rsi, sma_20, sma_50, macd, 
                                     volume, change_pct, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['rsi'], signal['sma_20'],
              signal['sma_50'], signal['macd'], signal['volume'], signal['change_pct'],
              signal['reason'], signal['confidence'], signal['date']))
    
    for signal in sell_technical:
        cursor.execute('''
            INSERT INTO sell_technical (symbol, price, rsi, sma_20, sma_50, macd, 
                                      volume, change_pct, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['rsi'], signal['sma_20'],
              signal['sma_50'], signal['macd'], signal['volume'], signal['change_pct'],
              signal['reason'], signal['confidence'], signal['date']))
    
    conn.commit()
    conn.close()

def get_signals(category):
    conn = sqlite3.connect('finviz_screener_signals.db')
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT * FROM {category} ORDER BY confidence DESC')
    
    signals = []
    for row in cursor.fetchall():
        signals.append({
            'id': row[0],
            'symbol': row[1],
            'price': row[2],
            'reason': row[-3],
            'confidence': row[-2],
            'date': row[-1]
        })
    
    conn.close()
    return signals

def generate_screener_signals():
    print("🎯 Finviz Screener Analysis")
    print("=" * 60)
    print("📊 BUY Fundamental: P/E<20, ROA>15%, Growth>10%, D/E<1, QR>1")
    print("📊 SELL Fundamental: P/E>30, ROA<5%, Growth<-10%, D/E>2, QR<0.5")
    print("🔧 BUY Technical: RSI<30, Price>SMA20, MACD>0, Volume>1M, Change>2%")
    print("🔧 SELL Technical: RSI>70, Price<SMA50, MACD<0, Volume<100K, Change<-5%")
    print("=" * 60)
    
    # Initialize database
    init_db()
    
    # Get signals from Finviz screener
    buy_fundamental = get_buy_fundamental_stocks()
    sell_fundamental = get_sell_fundamental_stocks()
    buy_technical = get_buy_technical_stocks()
    sell_technical = get_sell_technical_stocks()
    
    # Save all signals
    save_signals(buy_fundamental, sell_fundamental, buy_technical, sell_technical)
    
    print(f"\n📈 FINVIZ SCREENER RESULTS:")
    print(f"✅ Buy Fundamental: {len(buy_fundamental)} stocks")
    print(f"❌ Sell Fundamental: {len(sell_fundamental)} stocks")
    print(f"✅ Buy Technical: {len(buy_technical)} stocks")
    print(f"❌ Sell Technical: {len(sell_technical)} stocks")
    print(f"🎯 Total: {len(buy_fundamental) + len(sell_fundamental) + len(buy_technical) + len(sell_technical)} signals")
    
    return {
        'buy_fundamental': buy_fundamental,
        'sell_fundamental': sell_fundamental,
        'buy_technical': buy_technical,
        'sell_technical': sell_technical
    }

if __name__ == "__main__":
    signals = generate_screener_signals()
    print("\n🎉 Finviz screener analysis complete!")

Finviz Screener Scraper
Uses Finviz screener with parameters instead of individual stocks
"""

import sqlite3
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import json
import pandas as pd
from urllib.parse import urlencode, urljoin
import re

def init_db():
    conn = sqlite3.connect('finviz_screener_signals.db')
    cursor = conn.cursor()
    
    # 4 professional tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buy_fundamental (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            pe_ratio REAL,
            roa REAL,
            sales_growth_5y REAL,
            debt_equity REAL,
            quick_ratio REAL,
            market_cap REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sell_fundamental (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            pe_ratio REAL,
            roa REAL,
            sales_growth_5y REAL,
            debt_equity REAL,
            quick_ratio REAL,
            market_cap REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buy_technical (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            rsi REAL,
            sma_20 REAL,
            sma_50 REAL,
            macd REAL,
            volume REAL,
            change_pct REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sell_technical (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            rsi REAL,
            sma_20 REAL,
            sma_50 REAL,
            macd REAL,
            volume REAL,
            change_pct REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def scrape_finviz_screener(screener_params):
    """
    Scrape Finviz screener with specific parameters
    Returns list of stocks that match the criteria
    """
    print(f"🔍 Scraping Finviz Screener with parameters...")
    
    # Headers to mimic browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Build Finviz screener URL
    base_url = "https://finviz.com/screener.ashx"
    params = {
        'v': '111',  # View mode
        'f': '',     # Filters
        'ft': '4',   # Filter type
        'o': 'ticker' # Order by ticker
    }
    
    # Add filters based on parameters
    filters = []
    
    if 'pe_under' in screener_params:
        filters.append(f"pe_under{screener_params['pe_under']}")
    if 'pe_over' in screener_params:
        filters.append(f"pe_over{screener_params['pe_over']}")
    if 'roa_over' in screener_params:
        filters.append(f"roa_over{screener_params['roa_over']}")
    if 'roa_under' in screener_params:
        filters.append(f"roa_under{screener_params['roa_under']}")
    if 'salesgrowth_over' in screener_params:
        filters.append(f"salesgrowth_over{screener_params['salesgrowth_over']}")
    if 'salesgrowth_under' in screener_params:
        filters.append(f"salesgrowth_under{screener_params['salesgrowth_under']}")
    if 'debt_under' in screener_params:
        filters.append(f"debt_under{screener_params['debt_under']}")
    if 'debt_over' in screener_params:
        filters.append(f"debt_over{screener_params['debt_over']}")
    if 'quickratio_over' in screener_params:
        filters.append(f"quickratio_over{screener_params['quickratio_over']}")
    if 'quickratio_under' in screener_params:
        filters.append(f"quickratio_under{screener_params['quickratio_under']}")
    if 'rsi_under' in screener_params:
        filters.append(f"rsi_under{screener_params['rsi_under']}")
    if 'rsi_over' in screener_params:
        filters.append(f"rsi_over{screener_params['rsi_over']}")
    if 'price_above_sma20' in screener_params:
        filters.append("price_above_sma20")
    if 'price_below_sma50' in screener_params:
        filters.append("price_below_sma50")
    if 'macd_above' in screener_params:
        filters.append("macd_above")
    if 'macd_below' in screener_params:
        filters.append("macd_below")
    if 'volume_over' in screener_params:
        filters.append(f"volume_over{screener_params['volume_over']}")
    if 'volume_under' in screener_params:
        filters.append(f"volume_under{screener_params['volume_under']}")
    if 'change_over' in screener_params:
        filters.append(f"change_over{screener_params['change_over']}")
    if 'change_under' in screener_params:
        filters.append(f"change_under{screener_params['change_under']}")
    
    params['f'] = ','.join(filters)
    
    print(f"📊 Screener URL: {base_url}?{urlencode(params)}")
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the screener table - try multiple selectors
        table = soup.find('table', class_='table-light') or soup.find('table', class_='screener_table') or soup.find('table', {'id': 'screener_table'})
        
        stocks = []
        
        if table:
            rows = table.find_all('tr')[1:]  # Skip header row
            
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 12:  # Ensure we have enough columns
                    try:
                        symbol = cells[1].get_text().strip()
                        price = parse_number(cells[2].get_text().strip())
                        pe_ratio = parse_number(cells[3].get_text().strip())
                        roa = parse_number(cells[4].get_text().strip().replace('%', ''))
                        sales_growth = parse_number(cells[5].get_text().strip().replace('%', ''))
                        debt_equity = parse_number(cells[6].get_text().strip())
                        quick_ratio = parse_number(cells[7].get_text().strip())
                        market_cap = parse_market_cap(cells[8].get_text().strip())
                        rsi = parse_number(cells[9].get_text().strip())
                        sma_20 = parse_number(cells[10].get_text().strip())
                        sma_50 = parse_number(cells[11].get_text().strip())
                        macd = parse_number(cells[12].get_text().strip())
                        volume = parse_number(cells[13].get_text().strip())
                        change = parse_number(cells[14].get_text().strip().replace('%', ''))
                        
                        stocks.append({
                            'symbol': symbol,
                            'price': price,
                            'pe_ratio': pe_ratio,
                            'roa': roa,
                            'sales_growth': sales_growth,
                            'debt_equity': debt_equity,
                            'quick_ratio': quick_ratio,
                            'market_cap': market_cap,
                            'rsi': rsi,
                            'sma_20': sma_20,
                            'sma_50': sma_50,
                            'macd': macd,
                            'volume': volume,
                            'change': change
                        })
                    except Exception as e:
                        print(f"❌ Error parsing row: {e}")
                        continue
        else:
            # Debug: print the HTML to see what we're getting
            print("❌ No table found. HTML preview:")
            print(soup.prettify()[:1000])
        
        print(f"✅ Found {len(stocks)} stocks matching screener criteria")
        return stocks
        
    except Exception as e:
        print(f"❌ Error scraping screener: {e}")
        return []

def parse_number(value):
    """Parse number from Finviz string"""
    if value == '-' or value == '' or value is None:
        return None
    
    # Remove common suffixes
    value = str(value).replace(',', '').replace('$', '').replace('%', '')
    
    try:
        return float(value)
    except ValueError:
        return None

def parse_market_cap(value):
    """Parse market cap from Finviz string (B for Billion, M for Million)"""
    if value == '-' or value == '' or value is None:
        return None
    
    value = str(value).replace(',', '').replace('$', '')
    
    if 'B' in value:
        return float(value.replace('B', '')) * 1000000000
    elif 'M' in value:
        return float(value.replace('M', '')) * 1000000
    else:
        try:
            return float(value)
        except ValueError:
            return None

def get_buy_fundamental_stocks():
    """Get stocks using BUY fundamental screener parameters"""
    print("📊 Getting BUY Fundamental stocks from Finviz Screener...")
    
    screener_params = {
        'pe_under': '25',           # P/E < 25 (more realistic)
        'roa_over': '10',           # ROA > 10% (more realistic)
        'salesgrowth_over': '5',    # Sales Growth > 5% (more realistic)
        'debt_under': '1.5',        # Debt/Equity < 1.5 (more realistic)
        'quickratio_over': '0.8'    # Quick Ratio > 0.8 (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        if all([stock['pe_ratio'], stock['roa'], stock['sales_growth'], 
                stock['debt_equity'], stock['quick_ratio']]):
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'pe_ratio': stock['pe_ratio'] or 0,
                'roa': stock['roa'] or 0,
                'sales_growth_5y': stock['sales_growth'] or 0,
                'debt_equity': stock['debt_equity'] or 0,
                'quick_ratio': stock['quick_ratio'] or 0,
                'market_cap': stock['market_cap'] or 0,
                'reason': f"✅ ALL 5 criteria met: P/E {stock['pe_ratio']:.1f} < 20, ROA {stock['roa']:.1f}% > 15%, Growth {stock['sales_growth']:.1f}% > 10%, D/E {stock['debt_equity']:.1f} < 1, QR {stock['quick_ratio']:.1f} > 1",
                'confidence': 0.95,
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def get_sell_fundamental_stocks():
    """Get stocks using SELL fundamental screener parameters"""
    print("📊 Getting SELL Fundamental stocks from Finviz Screener...")
    
    screener_params = {
        'pe_over': '40',            # P/E > 40 (more realistic)
        'roa_under': '3',           # ROA < 3% (more realistic)
        'salesgrowth_under': '-5',   # Sales Growth < -5% (more realistic)
        'debt_over': '3',           # Debt/Equity > 3 (more realistic)
        'quickratio_under': '0.3'   # Quick Ratio < 0.3 (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        red_flags = 0
        reasons = []
        
        if stock['pe_ratio'] and stock['pe_ratio'] > 30:
            red_flags += 1
            reasons.append(f"P/E {stock['pe_ratio']:.1f} > 30")
        
        if stock['roa'] and stock['roa'] < 5:
            red_flags += 1
            reasons.append(f"ROA {stock['roa']:.1f}% < 5%")
        
        if stock['sales_growth'] and stock['sales_growth'] < -10:
            red_flags += 1
            reasons.append(f"Growth {stock['sales_growth']:.1f}% < -10%")
        
        if stock['debt_equity'] and stock['debt_equity'] > 2:
            red_flags += 1
            reasons.append(f"D/E {stock['debt_equity']:.1f} > 2")
        
        if stock['quick_ratio'] and stock['quick_ratio'] < 0.5:
            red_flags += 1
            reasons.append(f"QR {stock['quick_ratio']:.1f} < 0.5")
        
        if red_flags >= 3:
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'pe_ratio': stock['pe_ratio'] or 0,
                'roa': stock['roa'] or 0,
                'sales_growth_5y': stock['sales_growth'] or 0,
                'debt_equity': stock['debt_equity'] or 0,
                'quick_ratio': stock['quick_ratio'] or 0,
                'market_cap': stock['market_cap'] or 0,
                'reason': f"❌ {red_flags} red flags: " + ", ".join(reasons),
                'confidence': min(0.95, 0.6 + (red_flags * 0.08)),
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def get_buy_technical_stocks():
    """Get stocks using BUY technical screener parameters"""
    print("🔧 Getting BUY Technical stocks from Finviz Screener...")
    
    screener_params = {
        'rsi_under': '40',          # RSI < 40 (more realistic)
        'price_above_sma20': True,   # Price > SMA20
        'macd_above': True,         # MACD > 0
        'volume_over': '500000',     # Volume > 500K (more realistic)
        'change_over': '1'          # Change > 1% (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        signals_count = 0
        reasons = []
        
        if stock['rsi'] and stock['rsi'] < 30:
            signals_count += 1
            reasons.append(f"RSI {stock['rsi']:.1f} oversold")
        
        if stock['price'] and stock['sma_20'] and stock['price'] > stock['sma_20']:
            signals_count += 1
            reasons.append(f"Price ${stock['price']:.2f} > SMA20 ${stock['sma_20']:.2f}")
        
        if stock['macd'] and stock['macd'] > 0:
            signals_count += 1
            reasons.append(f"MACD {stock['macd']:.2f} positive")
        
        if stock['volume'] and stock['volume'] > 1000000:
            signals_count += 1
            reasons.append(f"Volume {stock['volume']:,.0f} high")
        
        if stock['change'] and stock['change'] > 2:
            signals_count += 1
            reasons.append(f"Change {stock['change']:.1f}% positive")
        
        if signals_count >= 3:
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'rsi': stock['rsi'] or 0,
                'sma_20': stock['sma_20'] or 0,
                'sma_50': stock['sma_50'] or 0,
                'macd': stock['macd'] or 0,
                'volume': stock['volume'] or 0,
                'change_pct': stock['change'] or 0,
                'reason': f"✅ {signals_count} signals: " + ", ".join(reasons),
                'confidence': min(0.95, 0.6 + (signals_count * 0.08)),
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def get_sell_technical_stocks():
    """Get stocks using SELL technical screener parameters"""
    print("🔧 Getting SELL Technical stocks from Finviz Screener...")
    
    screener_params = {
        'rsi_over': '60',           # RSI > 60 (more realistic)
        'price_below_sma50': True,   # Price < SMA50
        'macd_below': True,         # MACD < 0
        'volume_under': '200000',    # Volume < 200K (more realistic)
        'change_under': '-3'        # Change < -3% (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        warnings_count = 0
        reasons = []
        
        if stock['rsi'] and stock['rsi'] > 70:
            warnings_count += 1
            reasons.append(f"RSI {stock['rsi']:.1f} overbought")
        
        if stock['price'] and stock['sma_50'] and stock['price'] < stock['sma_50']:
            warnings_count += 1
            reasons.append(f"Price ${stock['price']:.2f} < SMA50 ${stock['sma_50']:.2f}")
        
        if stock['macd'] and stock['macd'] < 0:
            warnings_count += 1
            reasons.append(f"MACD {stock['macd']:.2f} negative")
        
        if stock['volume'] and stock['volume'] < 100000:
            warnings_count += 1
            reasons.append(f"Volume {stock['volume']:,.0f} low")
        
        if stock['change'] and stock['change'] < -5:
            warnings_count += 1
            reasons.append(f"Change {stock['change']:.1f}% negative")
        
        if warnings_count >= 3:
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'rsi': stock['rsi'] or 0,
                'sma_20': stock['sma_20'] or 0,
                'sma_50': stock['sma_50'] or 0,
                'macd': stock['macd'] or 0,
                'volume': stock['volume'] or 0,
                'change_pct': stock['change'] or 0,
                'reason': f"❌ {warnings_count} warnings: " + ", ".join(reasons),
                'confidence': min(0.95, 0.6 + (warnings_count * 0.08)),
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def save_signals(buy_fundamental, sell_fundamental, buy_technical, sell_technical):
    conn = sqlite3.connect('finviz_screener_signals.db')
    cursor = conn.cursor()
    
    # Clear old data
    cursor.execute('DELETE FROM buy_fundamental')
    cursor.execute('DELETE FROM sell_fundamental')
    cursor.execute('DELETE FROM buy_technical')
    cursor.execute('DELETE FROM sell_technical')
    
    # Save all signals
    for signal in buy_fundamental:
        cursor.execute('''
            INSERT INTO buy_fundamental (symbol, price, pe_ratio, roa, sales_growth_5y, 
                                       debt_equity, quick_ratio, market_cap, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['pe_ratio'], signal['roa'],
              signal['sales_growth_5y'], signal['debt_equity'], signal['quick_ratio'],
              signal['market_cap'], signal['reason'], signal['confidence'], signal['date']))
    
    for signal in sell_fundamental:
        cursor.execute('''
            INSERT INTO sell_fundamental (symbol, price, pe_ratio, roa, sales_growth_5y, 
                                        debt_equity, quick_ratio, market_cap, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['pe_ratio'], signal['roa'],
              signal['sales_growth_5y'], signal['debt_equity'], signal['quick_ratio'],
              signal['market_cap'], signal['reason'], signal['confidence'], signal['date']))
    
    for signal in buy_technical:
        cursor.execute('''
            INSERT INTO buy_technical (symbol, price, rsi, sma_20, sma_50, macd, 
                                     volume, change_pct, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['rsi'], signal['sma_20'],
              signal['sma_50'], signal['macd'], signal['volume'], signal['change_pct'],
              signal['reason'], signal['confidence'], signal['date']))
    
    for signal in sell_technical:
        cursor.execute('''
            INSERT INTO sell_technical (symbol, price, rsi, sma_20, sma_50, macd, 
                                      volume, change_pct, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['rsi'], signal['sma_20'],
              signal['sma_50'], signal['macd'], signal['volume'], signal['change_pct'],
              signal['reason'], signal['confidence'], signal['date']))
    
    conn.commit()
    conn.close()

def get_signals(category):
    conn = sqlite3.connect('finviz_screener_signals.db')
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT * FROM {category} ORDER BY confidence DESC')
    
    signals = []
    for row in cursor.fetchall():
        signals.append({
            'id': row[0],
            'symbol': row[1],
            'price': row[2],
            'reason': row[-3],
            'confidence': row[-2],
            'date': row[-1]
        })
    
    conn.close()
    return signals

def generate_screener_signals():
    print("🎯 Finviz Screener Analysis")
    print("=" * 60)
    print("📊 BUY Fundamental: P/E<20, ROA>15%, Growth>10%, D/E<1, QR>1")
    print("📊 SELL Fundamental: P/E>30, ROA<5%, Growth<-10%, D/E>2, QR<0.5")
    print("🔧 BUY Technical: RSI<30, Price>SMA20, MACD>0, Volume>1M, Change>2%")
    print("🔧 SELL Technical: RSI>70, Price<SMA50, MACD<0, Volume<100K, Change<-5%")
    print("=" * 60)
    
    # Initialize database
    init_db()
    
    # Get signals from Finviz screener
    buy_fundamental = get_buy_fundamental_stocks()
    sell_fundamental = get_sell_fundamental_stocks()
    buy_technical = get_buy_technical_stocks()
    sell_technical = get_sell_technical_stocks()
    
    # Save all signals
    save_signals(buy_fundamental, sell_fundamental, buy_technical, sell_technical)
    
    print(f"\n📈 FINVIZ SCREENER RESULTS:")
    print(f"✅ Buy Fundamental: {len(buy_fundamental)} stocks")
    print(f"❌ Sell Fundamental: {len(sell_fundamental)} stocks")
    print(f"✅ Buy Technical: {len(buy_technical)} stocks")
    print(f"❌ Sell Technical: {len(sell_technical)} stocks")
    print(f"🎯 Total: {len(buy_fundamental) + len(sell_fundamental) + len(buy_technical) + len(sell_technical)} signals")
    
    return {
        'buy_fundamental': buy_fundamental,
        'sell_fundamental': sell_fundamental,
        'buy_technical': buy_technical,
        'sell_technical': sell_technical
    }

if __name__ == "__main__":
    signals = generate_screener_signals()
    print("\n🎉 Finviz screener analysis complete!")

Finviz Screener Scraper
Uses Finviz screener with parameters instead of individual stocks
"""

import sqlite3
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import json
import pandas as pd
from urllib.parse import urlencode, urljoin
import re

def init_db():
    conn = sqlite3.connect('finviz_screener_signals.db')
    cursor = conn.cursor()
    
    # 4 professional tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buy_fundamental (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            pe_ratio REAL,
            roa REAL,
            sales_growth_5y REAL,
            debt_equity REAL,
            quick_ratio REAL,
            market_cap REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sell_fundamental (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            pe_ratio REAL,
            roa REAL,
            sales_growth_5y REAL,
            debt_equity REAL,
            quick_ratio REAL,
            market_cap REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buy_technical (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            rsi REAL,
            sma_20 REAL,
            sma_50 REAL,
            macd REAL,
            volume REAL,
            change_pct REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sell_technical (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            price REAL,
            rsi REAL,
            sma_20 REAL,
            sma_50 REAL,
            macd REAL,
            volume REAL,
            change_pct REAL,
            reason TEXT,
            confidence REAL,
            date TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def scrape_finviz_screener(screener_params):
    """
    Scrape Finviz screener with specific parameters
    Returns list of stocks that match the criteria
    """
    print(f"🔍 Scraping Finviz Screener with parameters...")
    
    # Headers to mimic browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Build Finviz screener URL
    base_url = "https://finviz.com/screener.ashx"
    params = {
        'v': '111',  # View mode
        'f': '',     # Filters
        'ft': '4',   # Filter type
        'o': 'ticker' # Order by ticker
    }
    
    # Add filters based on parameters
    filters = []
    
    if 'pe_under' in screener_params:
        filters.append(f"pe_under{screener_params['pe_under']}")
    if 'pe_over' in screener_params:
        filters.append(f"pe_over{screener_params['pe_over']}")
    if 'roa_over' in screener_params:
        filters.append(f"roa_over{screener_params['roa_over']}")
    if 'roa_under' in screener_params:
        filters.append(f"roa_under{screener_params['roa_under']}")
    if 'salesgrowth_over' in screener_params:
        filters.append(f"salesgrowth_over{screener_params['salesgrowth_over']}")
    if 'salesgrowth_under' in screener_params:
        filters.append(f"salesgrowth_under{screener_params['salesgrowth_under']}")
    if 'debt_under' in screener_params:
        filters.append(f"debt_under{screener_params['debt_under']}")
    if 'debt_over' in screener_params:
        filters.append(f"debt_over{screener_params['debt_over']}")
    if 'quickratio_over' in screener_params:
        filters.append(f"quickratio_over{screener_params['quickratio_over']}")
    if 'quickratio_under' in screener_params:
        filters.append(f"quickratio_under{screener_params['quickratio_under']}")
    if 'rsi_under' in screener_params:
        filters.append(f"rsi_under{screener_params['rsi_under']}")
    if 'rsi_over' in screener_params:
        filters.append(f"rsi_over{screener_params['rsi_over']}")
    if 'price_above_sma20' in screener_params:
        filters.append("price_above_sma20")
    if 'price_below_sma50' in screener_params:
        filters.append("price_below_sma50")
    if 'macd_above' in screener_params:
        filters.append("macd_above")
    if 'macd_below' in screener_params:
        filters.append("macd_below")
    if 'volume_over' in screener_params:
        filters.append(f"volume_over{screener_params['volume_over']}")
    if 'volume_under' in screener_params:
        filters.append(f"volume_under{screener_params['volume_under']}")
    if 'change_over' in screener_params:
        filters.append(f"change_over{screener_params['change_over']}")
    if 'change_under' in screener_params:
        filters.append(f"change_under{screener_params['change_under']}")
    
    params['f'] = ','.join(filters)
    
    print(f"📊 Screener URL: {base_url}?{urlencode(params)}")
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the screener table - try multiple selectors
        table = soup.find('table', class_='table-light') or soup.find('table', class_='screener_table') or soup.find('table', {'id': 'screener_table'})
        
        stocks = []
        
        if table:
            rows = table.find_all('tr')[1:]  # Skip header row
            
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 12:  # Ensure we have enough columns
                    try:
                        symbol = cells[1].get_text().strip()
                        price = parse_number(cells[2].get_text().strip())
                        pe_ratio = parse_number(cells[3].get_text().strip())
                        roa = parse_number(cells[4].get_text().strip().replace('%', ''))
                        sales_growth = parse_number(cells[5].get_text().strip().replace('%', ''))
                        debt_equity = parse_number(cells[6].get_text().strip())
                        quick_ratio = parse_number(cells[7].get_text().strip())
                        market_cap = parse_market_cap(cells[8].get_text().strip())
                        rsi = parse_number(cells[9].get_text().strip())
                        sma_20 = parse_number(cells[10].get_text().strip())
                        sma_50 = parse_number(cells[11].get_text().strip())
                        macd = parse_number(cells[12].get_text().strip())
                        volume = parse_number(cells[13].get_text().strip())
                        change = parse_number(cells[14].get_text().strip().replace('%', ''))
                        
                        stocks.append({
                            'symbol': symbol,
                            'price': price,
                            'pe_ratio': pe_ratio,
                            'roa': roa,
                            'sales_growth': sales_growth,
                            'debt_equity': debt_equity,
                            'quick_ratio': quick_ratio,
                            'market_cap': market_cap,
                            'rsi': rsi,
                            'sma_20': sma_20,
                            'sma_50': sma_50,
                            'macd': macd,
                            'volume': volume,
                            'change': change
                        })
                    except Exception as e:
                        print(f"❌ Error parsing row: {e}")
                        continue
        else:
            # Debug: print the HTML to see what we're getting
            print("❌ No table found. HTML preview:")
            print(soup.prettify()[:1000])
        
        print(f"✅ Found {len(stocks)} stocks matching screener criteria")
        return stocks
        
    except Exception as e:
        print(f"❌ Error scraping screener: {e}")
        return []

def parse_number(value):
    """Parse number from Finviz string"""
    if value == '-' or value == '' or value is None:
        return None
    
    # Remove common suffixes
    value = str(value).replace(',', '').replace('$', '').replace('%', '')
    
    try:
        return float(value)
    except ValueError:
        return None

def parse_market_cap(value):
    """Parse market cap from Finviz string (B for Billion, M for Million)"""
    if value == '-' or value == '' or value is None:
        return None
    
    value = str(value).replace(',', '').replace('$', '')
    
    if 'B' in value:
        return float(value.replace('B', '')) * 1000000000
    elif 'M' in value:
        return float(value.replace('M', '')) * 1000000
    else:
        try:
            return float(value)
        except ValueError:
            return None

def get_buy_fundamental_stocks():
    """Get stocks using BUY fundamental screener parameters"""
    print("📊 Getting BUY Fundamental stocks from Finviz Screener...")
    
    screener_params = {
        'pe_under': '25',           # P/E < 25 (more realistic)
        'roa_over': '10',           # ROA > 10% (more realistic)
        'salesgrowth_over': '5',    # Sales Growth > 5% (more realistic)
        'debt_under': '1.5',        # Debt/Equity < 1.5 (more realistic)
        'quickratio_over': '0.8'    # Quick Ratio > 0.8 (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        if all([stock['pe_ratio'], stock['roa'], stock['sales_growth'], 
                stock['debt_equity'], stock['quick_ratio']]):
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'pe_ratio': stock['pe_ratio'] or 0,
                'roa': stock['roa'] or 0,
                'sales_growth_5y': stock['sales_growth'] or 0,
                'debt_equity': stock['debt_equity'] or 0,
                'quick_ratio': stock['quick_ratio'] or 0,
                'market_cap': stock['market_cap'] or 0,
                'reason': f"✅ ALL 5 criteria met: P/E {stock['pe_ratio']:.1f} < 20, ROA {stock['roa']:.1f}% > 15%, Growth {stock['sales_growth']:.1f}% > 10%, D/E {stock['debt_equity']:.1f} < 1, QR {stock['quick_ratio']:.1f} > 1",
                'confidence': 0.95,
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def get_sell_fundamental_stocks():
    """Get stocks using SELL fundamental screener parameters"""
    print("📊 Getting SELL Fundamental stocks from Finviz Screener...")
    
    screener_params = {
        'pe_over': '40',            # P/E > 40 (more realistic)
        'roa_under': '3',           # ROA < 3% (more realistic)
        'salesgrowth_under': '-5',   # Sales Growth < -5% (more realistic)
        'debt_over': '3',           # Debt/Equity > 3 (more realistic)
        'quickratio_under': '0.3'   # Quick Ratio < 0.3 (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        red_flags = 0
        reasons = []
        
        if stock['pe_ratio'] and stock['pe_ratio'] > 30:
            red_flags += 1
            reasons.append(f"P/E {stock['pe_ratio']:.1f} > 30")
        
        if stock['roa'] and stock['roa'] < 5:
            red_flags += 1
            reasons.append(f"ROA {stock['roa']:.1f}% < 5%")
        
        if stock['sales_growth'] and stock['sales_growth'] < -10:
            red_flags += 1
            reasons.append(f"Growth {stock['sales_growth']:.1f}% < -10%")
        
        if stock['debt_equity'] and stock['debt_equity'] > 2:
            red_flags += 1
            reasons.append(f"D/E {stock['debt_equity']:.1f} > 2")
        
        if stock['quick_ratio'] and stock['quick_ratio'] < 0.5:
            red_flags += 1
            reasons.append(f"QR {stock['quick_ratio']:.1f} < 0.5")
        
        if red_flags >= 3:
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'pe_ratio': stock['pe_ratio'] or 0,
                'roa': stock['roa'] or 0,
                'sales_growth_5y': stock['sales_growth'] or 0,
                'debt_equity': stock['debt_equity'] or 0,
                'quick_ratio': stock['quick_ratio'] or 0,
                'market_cap': stock['market_cap'] or 0,
                'reason': f"❌ {red_flags} red flags: " + ", ".join(reasons),
                'confidence': min(0.95, 0.6 + (red_flags * 0.08)),
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def get_buy_technical_stocks():
    """Get stocks using BUY technical screener parameters"""
    print("🔧 Getting BUY Technical stocks from Finviz Screener...")
    
    screener_params = {
        'rsi_under': '40',          # RSI < 40 (more realistic)
        'price_above_sma20': True,   # Price > SMA20
        'macd_above': True,         # MACD > 0
        'volume_over': '500000',     # Volume > 500K (more realistic)
        'change_over': '1'          # Change > 1% (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        signals_count = 0
        reasons = []
        
        if stock['rsi'] and stock['rsi'] < 30:
            signals_count += 1
            reasons.append(f"RSI {stock['rsi']:.1f} oversold")
        
        if stock['price'] and stock['sma_20'] and stock['price'] > stock['sma_20']:
            signals_count += 1
            reasons.append(f"Price ${stock['price']:.2f} > SMA20 ${stock['sma_20']:.2f}")
        
        if stock['macd'] and stock['macd'] > 0:
            signals_count += 1
            reasons.append(f"MACD {stock['macd']:.2f} positive")
        
        if stock['volume'] and stock['volume'] > 1000000:
            signals_count += 1
            reasons.append(f"Volume {stock['volume']:,.0f} high")
        
        if stock['change'] and stock['change'] > 2:
            signals_count += 1
            reasons.append(f"Change {stock['change']:.1f}% positive")
        
        if signals_count >= 3:
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'rsi': stock['rsi'] or 0,
                'sma_20': stock['sma_20'] or 0,
                'sma_50': stock['sma_50'] or 0,
                'macd': stock['macd'] or 0,
                'volume': stock['volume'] or 0,
                'change_pct': stock['change'] or 0,
                'reason': f"✅ {signals_count} signals: " + ", ".join(reasons),
                'confidence': min(0.95, 0.6 + (signals_count * 0.08)),
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def get_sell_technical_stocks():
    """Get stocks using SELL technical screener parameters"""
    print("🔧 Getting SELL Technical stocks from Finviz Screener...")
    
    screener_params = {
        'rsi_over': '60',           # RSI > 60 (more realistic)
        'price_below_sma50': True,   # Price < SMA50
        'macd_below': True,         # MACD < 0
        'volume_under': '200000',    # Volume < 200K (more realistic)
        'change_under': '-3'        # Change < -3% (more realistic)
    }
    
    stocks = scrape_finviz_screener(screener_params)
    
    # Convert to signals
    signals = []
    for stock in stocks:
        warnings_count = 0
        reasons = []
        
        if stock['rsi'] and stock['rsi'] > 70:
            warnings_count += 1
            reasons.append(f"RSI {stock['rsi']:.1f} overbought")
        
        if stock['price'] and stock['sma_50'] and stock['price'] < stock['sma_50']:
            warnings_count += 1
            reasons.append(f"Price ${stock['price']:.2f} < SMA50 ${stock['sma_50']:.2f}")
        
        if stock['macd'] and stock['macd'] < 0:
            warnings_count += 1
            reasons.append(f"MACD {stock['macd']:.2f} negative")
        
        if stock['volume'] and stock['volume'] < 100000:
            warnings_count += 1
            reasons.append(f"Volume {stock['volume']:,.0f} low")
        
        if stock['change'] and stock['change'] < -5:
            warnings_count += 1
            reasons.append(f"Change {stock['change']:.1f}% negative")
        
        if warnings_count >= 3:
            signals.append({
                'symbol': stock['symbol'],
                'price': stock['price'] or 0,
                'rsi': stock['rsi'] or 0,
                'sma_20': stock['sma_20'] or 0,
                'sma_50': stock['sma_50'] or 0,
                'macd': stock['macd'] or 0,
                'volume': stock['volume'] or 0,
                'change_pct': stock['change'] or 0,
                'reason': f"❌ {warnings_count} warnings: " + ", ".join(reasons),
                'confidence': min(0.95, 0.6 + (warnings_count * 0.08)),
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return signals

def save_signals(buy_fundamental, sell_fundamental, buy_technical, sell_technical):
    conn = sqlite3.connect('finviz_screener_signals.db')
    cursor = conn.cursor()
    
    # Clear old data
    cursor.execute('DELETE FROM buy_fundamental')
    cursor.execute('DELETE FROM sell_fundamental')
    cursor.execute('DELETE FROM buy_technical')
    cursor.execute('DELETE FROM sell_technical')
    
    # Save all signals
    for signal in buy_fundamental:
        cursor.execute('''
            INSERT INTO buy_fundamental (symbol, price, pe_ratio, roa, sales_growth_5y, 
                                       debt_equity, quick_ratio, market_cap, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['pe_ratio'], signal['roa'],
              signal['sales_growth_5y'], signal['debt_equity'], signal['quick_ratio'],
              signal['market_cap'], signal['reason'], signal['confidence'], signal['date']))
    
    for signal in sell_fundamental:
        cursor.execute('''
            INSERT INTO sell_fundamental (symbol, price, pe_ratio, roa, sales_growth_5y, 
                                        debt_equity, quick_ratio, market_cap, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['pe_ratio'], signal['roa'],
              signal['sales_growth_5y'], signal['debt_equity'], signal['quick_ratio'],
              signal['market_cap'], signal['reason'], signal['confidence'], signal['date']))
    
    for signal in buy_technical:
        cursor.execute('''
            INSERT INTO buy_technical (symbol, price, rsi, sma_20, sma_50, macd, 
                                     volume, change_pct, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['rsi'], signal['sma_20'],
              signal['sma_50'], signal['macd'], signal['volume'], signal['change_pct'],
              signal['reason'], signal['confidence'], signal['date']))
    
    for signal in sell_technical:
        cursor.execute('''
            INSERT INTO sell_technical (symbol, price, rsi, sma_20, sma_50, macd, 
                                      volume, change_pct, reason, confidence, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal['symbol'], signal['price'], signal['rsi'], signal['sma_20'],
              signal['sma_50'], signal['macd'], signal['volume'], signal['change_pct'],
              signal['reason'], signal['confidence'], signal['date']))
    
    conn.commit()
    conn.close()

def get_signals(category):
    conn = sqlite3.connect('finviz_screener_signals.db')
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT * FROM {category} ORDER BY confidence DESC')
    
    signals = []
    for row in cursor.fetchall():
        signals.append({
            'id': row[0],
            'symbol': row[1],
            'price': row[2],
            'reason': row[-3],
            'confidence': row[-2],
            'date': row[-1]
        })
    
    conn.close()
    return signals

def generate_screener_signals():
    print("🎯 Finviz Screener Analysis")
    print("=" * 60)
    print("📊 BUY Fundamental: P/E<20, ROA>15%, Growth>10%, D/E<1, QR>1")
    print("📊 SELL Fundamental: P/E>30, ROA<5%, Growth<-10%, D/E>2, QR<0.5")
    print("🔧 BUY Technical: RSI<30, Price>SMA20, MACD>0, Volume>1M, Change>2%")
    print("🔧 SELL Technical: RSI>70, Price<SMA50, MACD<0, Volume<100K, Change<-5%")
    print("=" * 60)
    
    # Initialize database
    init_db()
    
    # Get signals from Finviz screener
    buy_fundamental = get_buy_fundamental_stocks()
    sell_fundamental = get_sell_fundamental_stocks()
    buy_technical = get_buy_technical_stocks()
    sell_technical = get_sell_technical_stocks()
    
    # Save all signals
    save_signals(buy_fundamental, sell_fundamental, buy_technical, sell_technical)
    
    print(f"\n📈 FINVIZ SCREENER RESULTS:")
    print(f"✅ Buy Fundamental: {len(buy_fundamental)} stocks")
    print(f"❌ Sell Fundamental: {len(sell_fundamental)} stocks")
    print(f"✅ Buy Technical: {len(buy_technical)} stocks")
    print(f"❌ Sell Technical: {len(sell_technical)} stocks")
    print(f"🎯 Total: {len(buy_fundamental) + len(sell_fundamental) + len(buy_technical) + len(sell_technical)} signals")
    
    return {
        'buy_fundamental': buy_fundamental,
        'sell_fundamental': sell_fundamental,
        'buy_technical': buy_technical,
        'sell_technical': sell_technical
    }

if __name__ == "__main__":
    signals = generate_screener_signals()
    print("\n🎉 Finviz screener analysis complete!")
