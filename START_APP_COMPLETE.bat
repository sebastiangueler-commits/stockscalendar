@echo off
echo ========================================
echo MAGIC STOCKS CALENDAR - COMPLETE SYSTEM
echo ========================================
echo.

echo 🚀 Starting Magic Stocks Calendar (Complete System)...
echo.

echo 📊 Activating virtual environment...
call venv\Scripts\activate.bat

echo 🔧 Starting simplified backend server on port 8001...
start "Backend Complete" cmd /k "venv\Scripts\activate.bat && python app_simple.py"

echo ⏳ Waiting 8 seconds for backend to start...
timeout /t 8 /nobreak > nul

echo 🌐 Starting React frontend on port 3000...
cd frontend
start "Frontend Complete" cmd /k "npm start"

echo ⏳ Waiting 15 seconds for frontend to start...
timeout /t 15 /nobreak > nul

echo 🌐 Opening complete application...
start http://localhost:3000

echo.
echo ✅ COMPLETE SYSTEM STARTED SUCCESSFULLY
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
echo 🎯 Complete Features:
echo    ✅ Landing page with features
echo    ✅ Login system
echo    ✅ Admin dashboard
echo    ✅ Historical & Fundamental calendars
echo    ✅ Payment system with PayPal
echo    ✅ Real-time system status
echo    ✅ Force update functionality
echo.
echo 🎨 Modern UI with:
echo    ✅ Professional design
echo    ✅ Responsive layout
echo    ✅ Dark theme
echo    ✅ Interactive elements
echo    ✅ Loading states
echo    ✅ Error handling
echo.
pause
