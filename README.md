# Telegram Auto-Responder - Worker

Telegram Worker для обработки диалогов и автоматических ответов с использованием AI.

## Требования

- Python 3.10+
- Telethon
- OpenAI API key

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Конфигурация

### 1. Создайте config.json

```json
{
  "WORK_FOLDER": "data",
  "PROCESSED_CLIENTS": "processed_clients.txt",
  "OPENAI": {
    "API_KEY": "your-openai-api-key",
    "MODEL": "gpt-4o-mini",
    "SYSTEM_TXT": "prompt.txt",
    "TARGET_CHATS": {
      "POSITIVE": "your-chat-id",
      "NEGATIVE": "your-chat-id"
    },
    "TRIGGER_PHRASES": {
      "POSITIVE": "[INTERESTED]",
      "NEGATIVE": "[NOT_INTERESTED]"
    }
  },
  "PROJECT_NAME": "Your Project",
  "TIMEZONE_OFFSET": 3
}
```

### 2. Создайте prompt.txt

Файл с системным промптом для AI.

### 3. (Опционально) Создайте api_map.txt

Если используете несколько аккаунтов:

```
session_name1.session api_id api_hash
session_name2.session api_id api_hash
```

### 4. (Опционально) Создайте proxies.txt

Если нужны прокси:

```
socks5://user:pass@host:port
http://host:port
```

## Добавление Telegram сессий

1. Положите `.session` файлы в папку `data/sessions/`
2. Для каждой сессии создайте `session_name.json`:

```json
{
  "api_id": 12345,
  "api_hash": "your_api_hash",
  "proxy": "socks5://user:pass@host:port"
}
```

## Запуск

```bash
python main.py
```

## Для Timeweb Cloud

При деплое на Timeweb:
- Тип приложения: **backend**
- Фреймворк: **docker** (или **another** если Docker не доступен)
- Команда запуска: `python main.py`

## Переменные окружения

Создайте следующие ENV переменные в Timeweb:
- `OPENAI_API_KEY` - ваш OpenAI API ключ
- Все остальное настраивается через `config.json`

## Структура данных

- `data/sessions/` - Telegram сессии (.session файлы)
- `data/convos/` - История диалогов
- `processed_clients.txt` - Обработанные пользователи
- `errors.log` - Лог ошибок
