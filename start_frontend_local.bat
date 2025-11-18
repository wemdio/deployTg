@echo off
echo ========================================
echo   Запуск Frontend (React)
echo ========================================
echo.

cd /d "%~dp0frontend"

echo [1/2] Проверка зависимостей...
if not exist "node_modules" (
    echo Установка npm зависимостей...
    npm install
    
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ❌ Ошибка установки зависимостей!
        echo Убедитесь что Node.js установлен: https://nodejs.org/
        pause
        exit /b 1
    )
) else (
    echo ✅ Зависимости уже установлены
)

echo.
echo [2/2] Запуск React приложения на http://localhost:3000
echo.
echo 🌐 Откроется в браузере автоматически
echo.
echo Нажмите Ctrl+C для остановки
echo ----------------------------------------
echo.

npm start

