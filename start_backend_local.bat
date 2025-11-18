@echo off
echo ========================================
echo   Запуск Backend (FastAPI)
echo ========================================
echo.

cd /d "%~dp0backend"

echo [1/3] Установка зависимостей...
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Ошибка установки зависимостей!
    pause
    exit /b 1
)

echo.
echo [2/3] Создание необходимых папок...
if not exist "data\sessions" mkdir data\sessions
if not exist "campaigns" mkdir campaigns
if not exist "campaigns_runtime" mkdir campaigns_runtime

echo.
echo [3/3] Запуск Backend API на http://localhost:8000
echo.
echo 📖 API Документация: http://localhost:8000/docs
echo 🔍 Альтернативная документация: http://localhost:8000/redoc
echo.
echo Нажмите Ctrl+C для остановки
echo ----------------------------------------
echo.

python run.py

