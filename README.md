# Telegram Auto-Responder - Backend + Worker

Backend API (FastAPI) + Worker (Telegram bot) для автоматизации ответов в Telegram с использованием AI.

## 🏗️ Архитектура

### Локально:
```
┌─────────────┐
│   Backend   │  ← FastAPI API + веб-интерфейс
│   (FastAPI) │  ← Создает config.json, запускает worker
└──────┬──────┘
       │ subprocess.Popen()
       ▼
┌─────────────┐
│   Worker    │  ← Telegram bot (main.py)
│  (Telethon) │  ← Читает config.json
└─────────────┘
```

### Timeweb Cloud:
- Backend **запускает Worker** как subprocess
- Worker **НЕ** отдельное приложение
- Управление через веб-интерфейс ✅

## 📦 Файлы

- `api.py` - точка входа для FastAPI (Timeweb Cloud)
- `run.py` - запуск backend для локальной разработки  
- `main.py` - **Worker** (Telegram bot), запускается backend'ом
- `app/` - код FastAPI приложения
- `requirements.txt` - зависимости для Backend + Worker

## 🚀 Деплой на Timeweb Cloud

### Настройки приложения:

- **Тип**: `backend`
- **Фреймворк**: `flask` или `docker`
- **Ветка**: `backend`
- **Команда сборки**: `pip install -r requirements.txt`
- **Команда запуска**: `uvicorn api:app --host 0.0.0.0 --port 8000`
- **Порт**: `8000`

### После деплоя:

1. ✅ Откройте веб-интерфейс (Frontend)
2. ✅ Создайте кампанию через интерфейс
3. ✅ Настройте OpenAI, Telegram каналы, задержки
4. ✅ Загрузите `.session` файлы через интерфейс
5. ✅ Запустите кампанию - Worker запустится автоматически!

**Всё управление через интерфейс!** Никаких ENV переменных не нужно! 🎉

## 💻 Локальная разработка

### Установка зависимостей:

```bash
pip install -r requirements.txt
```

### Запуск:

```bash
# Запуск Backend (FastAPI)
python run.py

# Worker запускается автоматически при старте кампании через интерфейс
```

Или используйте скрипт из корня проекта:
```bash
# Windows
start_all_local.bat

# Linux/Mac
./start_all.sh
```

## 📂 Структура проекта

```
backend/
├── api.py                    # Точка входа FastAPI (для Timeweb)
├── run.py                    # Запуск backend локально
├── main.py                   # Worker (Telegram bot)
├── requirements.txt          # Зависимости
├── app/                      # FastAPI приложение
│   ├── main.py              # FastAPI app
│   ├── models.py            # Pydantic модели
│   ├── database.py          # БД (JSON файлы)
│   ├── campaign_manager.py  # Запуск worker
│   └── api/                 # API endpoints
│       ├── campaigns.py
│       ├── accounts.py
│       └── dialogs.py
├── campaigns/               # Конфиги кампаний (JSON)
├── campaigns_runtime/       # Запущенные кампании
│   └── {campaign_id}/
│       ├── main.py          # Копия worker
│       ├── config.json      # Конфиг кампании
│       ├── prompt.txt       # AI промпт
│       ├── api_map.txt      # Telegram API credentials
│       ├── proxies.txt      # Прокси
│       └── data/
│           └── sessions/    # Telegram сессии
└── data/
    └── sessions/            # Загруженные .session файлы
```

## ⚙️ Как это работает

### 1. Пользователь создает кампанию через интерфейс:
- OpenAI API key, модель
- Target chats (куда пересылать)
- Trigger phrases (фразы для определения интереса)
- System prompt
- Задержки и таймауты

### 2. Backend создает конфиг:
```python
# campaign_manager.py создает:
campaigns_runtime/{campaign_id}/
  ├── config.json       # Все настройки из интерфейса
  ├── prompt.txt        # System prompt для AI
  ├── api_map.txt       # API credentials для аккаунтов
  ├── proxies.txt       # Прокси для аккаунтов
  └── data/sessions/    # Копии .session файлов
```

### 3. Backend запускает Worker:
```python
subprocess.Popen([
    sys.executable, "main.py"
], cwd=campaign_dir)
```

### 4. Worker читает config.json и работает:
- Подключается к Telegram аккаунтам
- Обрабатывает диалоги
- Генерирует ответы через OpenAI
- Пересылает диалоги в целевые чаты

## 🔒 Безопасность

⚠️ **НИКОГДА НЕ КОММИТЬТЕ В GIT:**
- `campaigns/*.json` (содержат API ключи)
- `campaigns_runtime/` (содержат конфиги с секретами)
- `*.session` файлы
- `data/sessions/` 

Все эти файлы уже в `.gitignore` ✅

## 📝 Настройки кампании (через интерфейс)

### OpenAI:
- API Key
- Model (gpt-4, gpt-4o-mini и т.д.)
- System Prompt
- Target Chats (Positive/Negative)
- Trigger Phrases
- Fallback settings

### Telegram:
- Forward limit
- History limit
- Reply only if previously wrote
- Delays (pre-read, read-reply, account loop и т.д.)
- Sleep periods (имитация человеческого режима)
- Timezone offset

### Accounts:
- Session files (.session)
- API credentials (api_id, api_hash)
- Proxies (опционально)

## 🆘 Troubleshooting

### Backend не запускается на Timeweb:
- Проверьте что команда запуска: `uvicorn api:app --host 0.0.0.0 --port 8000`
- Проверьте что порт 8000 открыт

### Worker не запускается:
- Проверьте логи кампании в интерфейсе
- Убедитесь что `main.py` есть в корне проекта
- Проверьте что все зависимости установлены

### Ошибка ModuleNotFoundError:
- Убедитесь что `requirements.txt` содержит все зависимости
- Пересоберите приложение на Timeweb

---

## ✅ Итого: Что деплоить на Timeweb?

1. **Backend** (ветка `backend`) - FastAPI + Worker внутри
2. **Frontend** (ветка `frontend`) - React интерфейс

**Worker НЕ нужен как отдельное приложение!** ❌

Управление через веб-интерфейс! 🎉
