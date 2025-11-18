#!/bin/bash

echo "================================"
echo "  TG Auto-Responder Backend"
echo "================================"
echo ""

# Создаем необходимые папки
mkdir -p backend/campaigns
mkdir -p backend/campaigns_runtime
mkdir -p backend/data/sessions

echo "✅ Directories created"
echo ""

# Запускаем FastAPI приложение
echo "🚀 Starting FastAPI server..."
echo "📖 API Documentation: /docs"
echo "================================"
echo ""

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1

