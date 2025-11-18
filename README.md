# 🤖 TG Auto-Responder

**Автоматический ответчик для Telegram** с интеграцией OpenAI GPT.

Управляйте несколькими Telegram аккаунтами, автоматически отвечайте на сообщения с помощью AI и отслеживайте заинтересованных пользователей.

---

## ✨ Возможности

- 🤖 **AI-ответы** - GPT генерирует умные ответы на сообщения
- 📱 **Множество аккаунтов** - управляйте несколькими Telegram аккаунтами
- 🎯 **Триггерные фразы** - автоматически определяет заинтересованных/незаинтересованных
- 📊 **Статистика** - отслеживание диалогов и обработанных клиентов
- 🔄 **Автозапуск** - кампании восстанавливаются после перезапуска
- 🌐 **Веб-интерфейс** - удобное управление через браузер
- 🔐 **Безопасность** - прокси для каждого аккаунта, хранение секретов в переменных окружения

---

## 🏗️ Архитектура

```
┌─────────────────┐
│   Frontend      │  ← React веб-интерфейс
│   (React)       │
└────────┬────────┘
         │ HTTP/REST API
         ▼
┌─────────────────┐
│   Backend       │  ← FastAPI сервер
│   (FastAPI)     │  ← Управление кампаниями
└────────┬────────┘
         │ subprocess
         ▼
┌─────────────────┐
│   Worker        │  ← Telegram Bot процесс
│   (Telethon)    │  ← Обработка сообщений
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│   Telegram      │     │   OpenAI API    │
│   API           │     │   (GPT-4)       │
└─────────────────┘     └─────────────────┘
```

---

## 🚀 Быстрый старт

### Локальная разработка

**1. Запустить всё сразу:**
```bash
start_all_local.bat
```

**2. Или по отдельности:**
```bash
# Backend
start_backend_local.bat

# Frontend
start_frontend_local.bat
```

Откроется:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### Деплой на Timeweb Cloud

**Подробная инструкция:** [DEPLOY_TIMEWEB.md](DEPLOY_TIMEWEB.md)

**Кратко:**

1. **Создать приложение на Timeweb:**
   - Тип: Backend
   - Фреймворк: FastAPI
   - Команда сборки: `pip install --no-cache-dir -r backend/requirements.txt`
   - Команда запуска: `bash backend/start.sh`

2. **Добавить переменные окружения:**
   ```bash
   OPENAI_API_KEY=sk-proj-ваш_ключ
   ```

3. **Задеплоить!** 🚀

---

## 📋 Требования

### Для разработки:
- Python 3.10+
- Node.js 16+
- OpenAI API ключ

### Для production:
- Timeweb Cloud аккаунт
- GitHub репозиторий
- OpenAI API ключ

---

## 📁 Структура проекта

```
tgrespNadeploy/
├── backend/                      # Backend приложение
│   ├── app/
│   │   ├── main.py              # FastAPI приложение
│   │   ├── campaign_manager.py  # Управление worker процессами
│   │   └── api/                 # API роутеры
│   │       ├── campaigns.py     # CRUD кампаний
│   │       ├── accounts.py      # Управление аккаунтами
│   │       └── dialogs.py       # История диалогов
│   ├── requirements.txt         # Python зависимости
│   ├── start.sh                 # Скрипт запуска
│   ├── campaigns/               # Конфиги кампаний (сохраняются)
│   ├── campaigns_runtime/       # Worker процессы (runtime)
│   └── data/
│       └── sessions/            # Telegram сессии
│
├── frontend/                     # React приложение
│   ├── src/
│   │   ├── App.js               # Главный компонент
│   │   ├── components/          # React компоненты
│   │   └── api/client.js        # API клиент
│   └── package.json
│
├── campaigns_runtime/            # Шаблон worker
│   └── {example}/
│       └── main.py              # Worker скрипт (Telethon)
│
├── .gitignore                    # Защита секретов
├── DEPLOY_TIMEWEB.md            # Инструкция по деплою
└── LOCAL_DEVELOPMENT.md         # Локальная разработка
```

---

## 🔌 API Endpoints

### Campaigns

```http
GET    /campaigns/              # Список кампаний
POST   /campaigns/              # Создать кампанию
GET    /campaigns/{id}          # Получить кампанию
PUT    /campaigns/{id}          # Обновить кампанию
DELETE /campaigns/{id}          # Удалить кампанию
POST   /campaigns/{id}/start    # Запустить
POST   /campaigns/{id}/stop     # Остановить
GET    /campaigns/{id}/status   # Статус
GET    /campaigns/{id}/logs     # Логи
GET    /campaigns/{id}/stats    # Статистика
```

### Accounts

```http
GET    /accounts/{campaign_id}                    # Список аккаунтов
POST   /accounts/{campaign_id}                    # Добавить аккаунт
PUT    /accounts/{campaign_id}/{session_name}     # Обновить
DELETE /accounts/{campaign_id}/{session_name}     # Удалить
POST   /accounts/{campaign_id}/upload-session     # Загрузить .session
POST   /accounts/{campaign_id}/upload-json        # Загрузить .json
GET    /accounts/available                        # Доступные сессии
```

### Dialogs

```http
GET    /dialogs/{campaign_id}                     # Список диалогов
GET    /dialogs/{campaign_id}/{session}/{user}    # История диалога
DELETE /dialogs/{campaign_id}/{session}/{user}    # Удалить диалог
GET    /dialogs/{campaign_id}/processed           # Обработанные клиенты
DELETE /dialogs/{campaign_id}/processed/{user}    # Удалить из processed
```

---

## 🔧 Конфигурация

### OpenAI настройки:

- `api_key` - OpenAI API ключ (обязательно!)
- `model` - Модель GPT (по умолчанию: gpt-4)
- `proxy` - HTTP прокси для OpenAI (опционально)
- `system_prompt` - Системный промпт для GPT
- `trigger_phrases` - Фразы для определения интереса/отказа

### Telegram настройки:

- `forward_limit` - Количество сообщений для пересылки
- `reply_only_if_previously_wrote` - Отвечать только в активных диалогах
- `pre_read_delay_range` - Задержка перед прочтением
- `read_reply_delay_range` - Задержка между прочтением и ответом
- `sleep_periods` - Периоды сна (например: `["20:00-08:00"]`)

---

## 🔐 Безопасность

### ⚠️ ВАЖНО: Не храните секреты в Git!

**Защищено через `.gitignore`:**
- ❌ `config.json` - конфиги с ключами
- ❌ `*.session` - Telegram сессии
- ❌ `api_map.txt` - API credentials
- ❌ `*.log` - логи

**Используйте переменные окружения:**
```bash
# В Timeweb Dashboard → Переменные
OPENAI_API_KEY=sk-proj-...
```

**Если случайно закоммитили секреты:**
1. Отзовите все ключи немедленно
2. Создайте новые
3. Очистите Git историю

---

## 📊 Мониторинг

### Health Check:
```bash
curl https://ваш-домен.twc1.net/health
```

### Статистика кампании:
```bash
curl https://ваш-домен.twc1.net/campaigns/{id}/stats
```

### Логи:
```bash
curl https://ваш-домен.twc1.net/campaigns/{id}/logs?limit=100
```

---

## 🐛 Troubleshooting

### Backend не запускается
- Проверьте логи в Timeweb Dashboard
- Убедитесь что все зависимости установлены
- Проверьте `requirements.txt`

### Worker не стартует
- Проверьте есть ли аккаунты в кампании
- Проверьте OpenAI ключ
- Проверьте логи: `/campaigns/{id}/logs`

### Сессия Telegram не работает
- Сессия может устареть (нужна переавторизация)
- Проверьте прокси если используется
- Проверьте `api_id` и `api_hash`

---

## 🎓 Примеры использования

### Создать кампанию:

```bash
curl -X POST https://ваш-домен.twc1.net/campaigns/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Моя первая кампания",
    "openai_settings": {
      "api_key": "sk-proj-...",
      "model": "gpt-4",
      "system_prompt": "Ты вежливый ассистент..."
    }
  }'
```

### Загрузить сессию:

```bash
curl -X POST https://ваш-домен.twc1.net/accounts/{campaign_id}/upload-session \
  -F "session_file=@194453263.session"
```

### Запустить кампанию:

```bash
curl -X POST https://ваш-домен.twc1.net/campaigns/{campaign_id}/start
```

---

## 📝 Лицензия

MIT License - используйте свободно!

---

## 🤝 Поддержка

- 📖 **Документация:** См. [DEPLOY_TIMEWEB.md](DEPLOY_TIMEWEB.md) и [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md)
- 🐛 **Issues:** Создайте issue в GitHub
- 💬 **Вопросы:** Напишите в issues

---

## 🎯 Roadmap

- [ ] WebSocket real-time обновления
- [ ] База данных вместо JSON файлов
- [ ] Множественные языки промптов
- [ ] Статистика и аналитика
- [ ] Telegram Bot для управления
- [ ] Docker контейнеризация

---

**Сделано с ❤️ для автоматизации Telegram**

🚀 **Начните прямо сейчас:** [DEPLOY_TIMEWEB.md](DEPLOY_TIMEWEB.md)

