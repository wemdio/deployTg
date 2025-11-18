@echo off
echo ========================================
echo   Запуск всего приложения
echo ========================================
echo.
echo Запускаем Backend и Frontend в отдельных окнах...
echo.

REM Запускаем Backend в новом окне
start "Backend API" cmd /k "call "%~dp0start_backend_local.bat""

REM Ждем 3 секунды чтобы Backend успел запуститься
timeout /t 3 /nobreak > nul

REM Запускаем Frontend в новом окне
start "Frontend React" cmd /k "call "%~dp0start_frontend_local.bat""

echo.
echo ✅ Приложения запускаются в отдельных окнах!
echo.
echo 📊 Backend API: http://localhost:8000
echo 🌐 Frontend: http://localhost:3000
echo.
echo Закройте окна терминалов для остановки приложений
echo.
pause

