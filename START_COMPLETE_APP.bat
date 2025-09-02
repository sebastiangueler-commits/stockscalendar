@echo off
echo ========================================
echo    MAGIC STOCKS CALENDAR - COMPLETO
echo ========================================
echo.
echo Iniciando sistema completo...
echo.

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Iniciar backend
echo Iniciando backend...
start "Backend" cmd /k "python -m uvicorn app:app --host 0.0.0.0 --port 8001"

REM Esperar un momento
timeout /t 3 /nobreak > nul

REM Iniciar frontend
echo Iniciando frontend...
cd frontend
start "Frontend" cmd /k "npm start"

echo.
echo ========================================
echo    SISTEMA INICIADO EXITOSAMENTE
echo ========================================
echo.
echo Backend: http://localhost:8001
echo Frontend: http://localhost:3000
echo.
echo Credenciales:
echo - Admin: admin@magicstocks.com / admin123
echo - User: user@magicstocks.com / user123
echo.
echo Presiona cualquier tecla para salir...
pause > nul
