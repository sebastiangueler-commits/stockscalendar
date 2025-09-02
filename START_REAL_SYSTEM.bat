@echo off
echo ========================================
echo MAGIC STOCKS CALENDAR - REAL SYSTEM
echo ========================================
echo.

echo 🚀 Starting Magic Stocks Calendar (REAL DATA SYSTEM)...
echo.

echo 📊 Activating virtual environment...
call venv\Scripts\activate.bat

echo 🔧 Starting REAL backend server on port 8001...
start "Backend REAL" cmd /k "venv\Scripts\activate.bat && python app_real.py"

echo ⏳ Waiting 10 seconds for backend to start...
timeout /t 10 /nobreak > nul

echo 🌐 Starting React frontend on port 3000...
cd frontend
start "Frontend REAL" cmd /k "npm start"

echo ⏳ Waiting 20 seconds for frontend to start...
timeout /t 20 /nobreak > nul

echo 🌐 Opening REAL application...
start http://localhost:3000

echo.
echo ✅ REAL SYSTEM STARTED SUCCESSFULLY
echo.
echo 📋 Available URLs:
echo    Frontend React: http://localhost:3000
echo    Backend API: http://localhost:8001
echo    API Docs: http://localhost:8001/docs
echo.
echo 🔐 Login Credentials:
echo    Admin: admin@magicstocks.com / admin123
echo    User: user@magicstocks.com / user123
echo.
echo 🎯 REAL Features:
echo    ✅ REAL stock data from multiple APIs
echo    ✅ Alpha Vantage, IEX Cloud, Finnhub
echo    ✅ Live market data
echo    ✅ Real-time analysis
echo    ✅ PayPal integration
echo    ✅ Complete frontend
echo.
echo 📈 APIs Used:
echo    ✅ Alpha Vantage (Primary)
echo    ✅ IEX Cloud (Backup)
echo    ✅ Finnhub (Fallback)
echo.
echo 💳 PayPal Integration:
echo    ✅ Sandbox mode (change to live for production)
echo    ✅ Real payment processing
echo.
pause
