#!/bin/bash

echo "================================"
echo "  TG Auto-Responder Backend"
echo "================================"
echo ""

# Переходим в папку backend
cd backend || exit 1

# Создаем необходимые папки
mkdir -p campaigns
mkdir -p campaigns_runtime
mkdir -p data/sessions

echo "✅ Directories created"
echo ""

# Запускаем FastAPI приложение
echo "🚀 Starting FastAPI server..."
echo "📖 API Documentation: /docs"
echo "================================"
echo ""

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1

