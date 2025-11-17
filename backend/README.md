# Telegram Auto-Responder - Backend API

FastAPI backend для управления кампаниями и аккаунтами Telegram.

## Требования

- Python 3.10+
- FastAPI
- Uvicorn

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск

### Локально
```bash
python run.py
```

### Для продакшена (Timeweb)
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Переменные окружения

Backend не требует дополнительных переменных окружения.
Данные хранятся в локальных JSON файлах.

## API Endpoints

- `GET /` - Информация об API
- `GET /health` - Health check
- `GET /api/campaigns` - Список кампаний
- `POST /api/campaigns` - Создать кампанию
- `GET /api/accounts` - Список аккаунтов
- `POST /api/accounts` - Добавить аккаунт
- `WebSocket /ws` - Real-time обновления

## Документация API

После запуска доступна по адресу:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

