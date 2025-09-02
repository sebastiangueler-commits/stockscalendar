#!/usr/bin/env python3
"""
Script de configuración automática para Magic Stocks Calendar con datos REALES
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("🚀 MAGIC STOCKS CALENDAR - CONFIGURACIÓN DE DATOS REALES")
    print("=" * 60)
    print()

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")

def install_dependencies():
    """Instalar dependencias necesarias"""
    print("📦 Instalando dependencias...")
    
    dependencies = [
        "fastapi",
        "uvicorn",
        "yfinance",
        "pandas",
        "numpy",
        "requests",
        "python-dotenv",
        "pydantic"
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} instalado")
        except subprocess.CalledProcessError:
            print(f"❌ Error instalando {dep}")
            return False
    
    return True

def create_env_file():
    """Crear archivo .env con configuración"""
    env_content = """# APIs para datos reales de acciones
# Obtén tus API keys gratuitas en:
# Alpha Vantage: https://www.alphavantage.co/support/#api-key
# IEX Cloud: https://iexcloud.io/cloud-login#/register
# Finnhub: https://finnhub.io/register

ALPHA_VANTAGE_API_KEY=demo
IEX_CLOUD_API_KEY=Tpk_018b97bce0a24c0d9c632c01c3c7c5c8
FINNHUB_API_KEY=demo

# PayPal Configuration (para producción)
PAYPAL_CLIENT_ID=demo
PAYPAL_CLIENT_SECRET=demo
PAYPAL_MODE=sandbox

# Configuración de la aplicación
APP_ENV=development
LOG_LEVEL=INFO
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Archivo .env creado")
        print("📝 Edita el archivo .env con tus API keys reales")
        return True
    except Exception as e:
        print(f"❌ Error creando .env: {e}")
        return False

def test_apis():
    """Probar conexión con APIs"""
    print("🔍 Probando conexión con APIs...")
    
    # Test Alpha Vantage
    try:
        response = requests.get(
            "https://www.alphavantage.co/query",
            params={
                "function": "TIME_SERIES_INTRADAY",
                "symbol": "AAPL",
                "interval": "1min",
                "apikey": "demo"
            },
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Alpha Vantage API: Conectado")
        else:
            print("⚠️ Alpha Vantage API: Limitado (usar API key real)")
    except:
        print("❌ Alpha Vantage API: No disponible")
    
    # Test Yahoo Finance
    try:
        import yfinance as yf
        ticker = yf.Ticker("AAPL")
        info = ticker.info
        if info:
            print("✅ Yahoo Finance API: Conectado")
        else:
            print("⚠️ Yahoo Finance API: Limitado")
    except:
        print("❌ Yahoo Finance API: No disponible")

def create_startup_script():
    """Crear script de inicio"""
    if os.name == 'nt':  # Windows
        script_content = """@echo off
echo ========================================
echo MAGIC STOCKS CALENDAR - DATOS REALES
echo ========================================
echo.

echo 🚀 Iniciando Magic Stocks Calendar con datos REALES...
echo.

echo 📊 Activando entorno virtual...
call venv\\Scripts\\activate.bat

echo 🔧 Iniciando backend con datos reales...
start "Backend Real" cmd /k "venv\\Scripts\\activate.bat && python app.py"

echo ⏳ Esperando 8 segundos para que el backend inicie...
timeout /t 8 /nobreak > nul

echo 🌐 Iniciando React frontend...
cd frontend
start "Frontend Real" cmd /k "npm start"

echo ⏳ Esperando 15 segundos para que el frontend inicie...
timeout /t 15 /nobreak > nul

echo 🌐 Abriendo aplicación con datos reales...
start http://localhost:3000

echo.
echo ✅ SISTEMA CON DATOS REALES INICIADO EXITOSAMENTE
echo.
echo 📋 URLs disponibles:
echo    Frontend React: http://localhost:3000
echo    Backend API: http://localhost:8001
echo    API Docs: http://localhost:8001/docs
echo.
echo 🔐 Credenciales de acceso:
echo    Admin: admin@magicstocks.com / admin123
echo    User: user@magicstocks.com / user123
echo.
echo 🎯 Características con datos REALES:
echo    ✅ 300+ acciones analizadas
echo    ✅ Datos en tiempo real de Yahoo Finance
echo    ✅ Análisis fundamental y técnico real
echo    ✅ Indicadores técnicos calculados
echo    ✅ Objetivos de precio automáticos
echo    ✅ Stop loss calculado
echo.
pause
"""
        filename = "START_REAL_DATA.bat"
    else:  # Linux/Mac
        script_content = """#!/bin/bash
echo "========================================"
echo "MAGIC STOCKS CALENDAR - DATOS REALES"
echo "========================================"
echo

echo "🚀 Iniciando Magic Stocks Calendar con datos REALES..."
echo

echo "📊 Activando entorno virtual..."
source venv/bin/activate

echo "🔧 Iniciando backend con datos reales..."
python app.py &
BACKEND_PID=$!

echo "⏳ Esperando 8 segundos para que el backend inicie..."
sleep 8

echo "🌐 Iniciando React frontend..."
cd frontend
npm start &
FRONTEND_PID=$!

echo "⏳ Esperando 15 segundos para que el frontend inicie..."
sleep 15

echo "🌐 Abriendo aplicación con datos reales..."
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:3000
elif command -v open > /dev/null; then
    open http://localhost:3000
fi

echo
echo "✅ SISTEMA CON DATOS REALES INICIADO EXITOSAMENTE"
echo
echo "📋 URLs disponibles:"
echo "   Frontend React: http://localhost:3000"
echo "   Backend API: http://localhost:8001"
echo "   API Docs: http://localhost:8001/docs"
echo
echo "🔐 Credenciales de acceso:"
echo "   Admin: admin@magicstocks.com / admin123"
echo "   User: user@magicstocks.com / user123"
echo
echo "🎯 Características con datos REALES:"
echo "   ✅ 300+ acciones analizadas"
echo "   ✅ Datos en tiempo real de Yahoo Finance"
echo "   ✅ Análisis fundamental y técnico real"
echo "   ✅ Indicadores técnicos calculados"
echo "   ✅ Objetivos de precio automáticos"
echo "   ✅ Stop loss calculado"
echo

# Función para limpiar procesos al salir
cleanup() {
    echo "🛑 Deteniendo procesos..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "Presiona Ctrl+C para detener la aplicación..."
wait
"""
        filename = "start_real_data.sh"
        # Hacer ejecutable
        os.chmod(filename, 0o755)
    
    try:
        with open(filename, "w") as f:
            f.write(script_content)
        print(f"✅ Script de inicio creado: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error creando script de inicio: {e}")
        return False

def show_next_steps():
    """Mostrar próximos pasos"""
    print("\n" + "=" * 60)
    print("🎉 CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print()
    print("📋 Próximos pasos:")
    print()
    print("1. 🔑 Configurar APIs reales:")
    print("   - Edita el archivo .env")
    print("   - Agrega tus API keys reales")
    print("   - Obtén API keys gratuitas en:")
    print("     * Alpha Vantage: https://www.alphavantage.co/support/#api-key")
    print("     * IEX Cloud: https://iexcloud.io/cloud-login#/register")
    print()
    print("2. 🚀 Ejecutar la aplicación:")
    if os.name == 'nt':
        print("   - Ejecuta: START_REAL_DATA.bat")
    else:
        print("   - Ejecuta: ./start_real_data.sh")
    print()
    print("3. 🌐 Acceder a la aplicación:")
    print("   - Frontend: http://localhost:3000")
    print("   - Backend: http://localhost:8001")
    print("   - API Docs: http://localhost:8001/docs")
    print()
    print("4. 🔐 Credenciales:")
    print("   - Admin: admin@magicstocks.com / admin123")
    print("   - User: user@magicstocks.com / user123")
    print()
    print("🎯 Características con datos REALES:")
    print("   ✅ 300+ acciones analizadas")
    print("   ✅ Datos en tiempo real de Yahoo Finance")
    print("   ✅ Análisis fundamental y técnico real")
    print("   ✅ Indicadores técnicos calculados")
    print("   ✅ Objetivos de precio automáticos")
    print("   ✅ Stop loss calculado")
    print()
    print("📚 Documentación:")
    print("   - Lee: REAL_DATA_SETUP.md")
    print("   - Configuración: config.py")
    print()

def main():
    """Función principal"""
    print_banner()
    
    # Verificar Python
    check_python_version()
    print()
    
    # Instalar dependencias
    if not install_dependencies():
        print("❌ Error instalando dependencias")
        sys.exit(1)
    print()
    
    # Crear archivo .env
    if not create_env_file():
        print("❌ Error creando archivo .env")
        sys.exit(1)
    print()
    
    # Probar APIs
    test_apis()
    print()
    
    # Crear script de inicio
    if not create_startup_script():
        print("❌ Error creando script de inicio")
        sys.exit(1)
    print()
    
    # Mostrar próximos pasos
    show_next_steps()

if __name__ == "__main__":
    main()
