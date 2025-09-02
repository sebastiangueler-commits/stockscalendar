@echo off
echo ========================================
echo MAGIC STOCKS CALENDAR - SIMPLIFICADO
echo ========================================
echo.

echo 🚀 Iniciando Magic Stocks Calendar (Simplificado)...
echo.

echo 📊 Activando entorno virtual...
call venv\Scripts\activate.bat

echo 🔧 Iniciando servidor backend simplificado en puerto 8001...
start "Backend Simple" cmd /k "venv\Scripts\activate.bat && python app_simple.py"

echo ⏳ Esperando 5 segundos para que el backend inicie...
timeout /t 5 /nobreak > nul

echo 🌐 Iniciando frontend React en puerto 3000...
cd frontend
start "Frontend" cmd /k "npm start"

echo ⏳ Esperando 10 segundos para que el frontend inicie...
timeout /t 10 /nobreak > nul

echo 🌐 Abriendo aplicación completa...
start http://localhost:3000

echo.
echo ✅ APLICACIÓN SIMPLIFICADA INICIADA
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
echo 🎯 Sistema simplificado sin rate limiting
echo 📈 3000 acciones analizadas con datos realistas
echo.
pause
