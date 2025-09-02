@echo off
echo ========================================
echo MAGIC STOCKS CALENDAR - DEFINITIVO
echo ========================================
echo.

echo 🚀 Iniciando Magic Stocks Calendar...
echo.

echo 📊 Activando entorno virtual...
call venv\Scripts\activate.bat

echo 🔧 Iniciando servidor backend en puerto 8001...
start "Backend" cmd /k "venv\Scripts\activate.bat && python app.py"

echo ⏳ Esperando 8 segundos para que el backend inicie...
timeout /t 8 /nobreak > nul

echo 🌐 Iniciando frontend React en puerto 3000...
cd frontend
start "Frontend" cmd /k "npm start"

echo ⏳ Esperando 15 segundos para que el frontend inicie...
timeout /t 15 /nobreak > nul

echo 🌐 Abriendo aplicación completa...
start http://localhost:3000

echo.
echo ✅ APLICACIÓN DEFINITIVA INICIADA
echo.
echo 📋 URLs disponibles:
echo    Frontend React: http://localhost:3000
echo    Backend API: http://localhost:8001
echo    API Docs: http://localhost:8001/docs
echo.
echo 🔐 Credenciales:
echo    Email: admin@magicstocks.com
echo    Contraseña: admin123
echo.
pause
