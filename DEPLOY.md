# 🚀 Инструкция по настройке Worker на Timeweb Cloud

## Способ 1: SSH подключение (Рекомендуется)

### Шаг 1: Получите SSH доступ

1. Зайдите в **Панель Timeweb Cloud** → Ваши приложения → **TG Responder - Worker**
2. Найдите раздел **SSH доступ** или **Терминал**
3. Скопируйте команду для подключения (обычно вида):
   ```bash
   ssh username@wemdio-deploytg-f0fb.twc1.net
   ```

### Шаг 2: Подключитесь к серверу

Откройте терминал на вашем компьютере и выполните:
```bash
ssh username@wemdio-deploytg-f0fb.twc1.net
```

### Шаг 3: Перейдите в папку приложения

```bash
cd /app
# или
cd ~/app
```

### Шаг 4: Запустите скрипт инициализации

```bash
bash setup.sh
```

Этот скрипт:
- Создаст `config.json` из примера
- Автоматически подставит `OPENAI_API_KEY` из переменных окружения
- Создаст необходимые папки
- Создаст `prompt.txt` из примера

### Шаг 5: Отредактируйте конфигурацию

```bash
# Откройте config.json в редакторе
nano config.json
# или
vi config.json
```

**Обязательно измените**:
- `TARGET_CHATS.POSITIVE` - куда отправлять заинтересованных клиентов
- `TARGET_CHATS.NEGATIVE` - куда отправлять отказавшихся
- `PROJECT_NAME` - название вашего проекта

**Сохраните**: `Ctrl+O`, `Enter`, `Ctrl+X` (для nano)

### Шаг 6: Настройте промпт

```bash
nano prompt.txt
```

Напишите системный промпт для AI-ассистента.

### Шаг 7: Загрузите Telegram сессии

Используйте SCP или SFTP для загрузки файлов:

```bash
# С вашего компьютера:
scp ваша_сессия.session username@wemdio-deploytg-f0fb.twc1.net:/app/data/sessions/
scp ваша_сессия.json username@wemdio-deploytg-f0fb.twc1.net:/app/data/sessions/
```

Или используйте SFTP клиент (FileZilla, WinSCP):
- Host: `wemdio-deploytg-f0fb.twc1.net`
- Port: `22`
- Загрузите файлы в `/app/data/sessions/`

### Шаг 8: (Опционально) Настройте api_map.txt

Если используете несколько аккаунтов:

```bash
nano api_map.txt
```

Формат:
```
1234567890.session 12345678 abcdef1234567890abcdef1234567890
```

### Шаг 9: Перезапустите приложение

В панели Timeweb Cloud:
1. Перейдите в **TG Responder - Worker**
2. Нажмите **Перезапустить**

---

## Способ 2: Через веб-интерфейс Timeweb

### Шаг 1: Файловый менеджер

1. Зайдите в **Панель Timeweb Cloud** → **TG Responder - Worker**
2. Найдите **Файловый менеджер** или **File Manager**
3. Перейдите в папку приложения (обычно `/app`)

### Шаг 2: Создайте файлы вручную

#### config.json
Нажмите **Создать файл** → `config.json` и вставьте:
```json
{
  "WORK_FOLDER": "data",
  "PROCESSED_CLIENTS": "processed_clients.txt",
  "OPENAI": {
    "API_KEY": "sk-ваш-ключ-здесь",
    "MODEL": "gpt-4o-mini",
    "SYSTEM_TXT": "prompt.txt",
    "PROXY": null,
    "TARGET_CHATS": {
      "POSITIVE": "@ваш_канал",
      "NEGATIVE": "@ваш_канал"
    },
    "TRIGGER_PHRASES": {
      "POSITIVE": "[INTERESTED]",
      "NEGATIVE": "[NOT_INTERESTED]"
    },
    "USE_FALLBACK_ON_OPENAI_FAIL": false,
    "FALLBACK_TEXT": ""
  },
  "PROJECT_NAME": "Мой проект",
  "TELEGRAM_FORWARD_LIMIT": 5,
  "TELEGRAM_HISTORY_LIMIT": 100,
  "REPLY_ONLY_IF_PREVIOUSLY_WROTE": true,
  "PRE_READ_DELAY_RANGE": [2, 5],
  "READ_REPLY_DELAY_RANGE": [3, 8],
  "ACCOUNT_LOOP_DELAY_RANGE": [60, 120],
  "CHECK_NEW_MSG_INTERVAL_RANGE": [5, 10],
  "DIALOG_WAIT_WINDOW_RANGE": [30, 60],
  "SLEEP_PERIODS": ["21:00-08:00"],
  "TIMEZONE_OFFSET": 3
}
```

#### prompt.txt
Нажмите **Создать файл** → `prompt.txt` и вставьте ваш промпт.

### Шаг 3: Загрузите сессии

Используйте **Upload файлов** в файловом менеджере:
1. Создайте папку `data/sessions/`
2. Загрузите `.session` и `.json` файлы

### Шаг 4: Перезапустите

Нажмите **Перезапустить** в панели приложения.

---

## Способ 3: Автоматический через Git (Самый простой!)

Этот способ уже реализован! После деплоя приложение автоматически:
1. Создаст папки `data/sessions/` и `data/convos/`
2. Скопирует `config.example.json` → `config.json`
3. Подставит `OPENAI_API_KEY` из ENV переменной

**Вам нужно только**:
1. Добавить `OPENAI_API_KEY` в переменные окружения Timeweb
2. Через SSH или файловый менеджер отредактировать `config.json` (TARGET_CHATS, PROJECT_NAME)
3. Загрузить Telegram сессии в `data/sessions/`
4. Перезапустить приложение

---

## 🔐 Важно про переменные окружения

В панели Timeweb обязательно добавьте:
- **Ключ**: `OPENAI_API_KEY`
- **Значение**: ваш OpenAI API ключ

**Не храните секретные ключи в config.json!** Используйте ENV переменные.

---

## 📁 Структура файлов после настройки

```
/app/
├── main.py                    # Основной скрипт
├── requirements.txt           # Зависимости
├── config.json               # ✏️ Ваша конфигурация
├── prompt.txt                # ✏️ Ваш промпт
├── api_map.txt              # ✏️ (опционально) API credentials
├── proxies.txt              # ✏️ (опционально) Прокси
├── processed_clients.txt     # Обработанные пользователи
├── data/
│   ├── sessions/            # ✏️ Ваши .session и .json файлы
│   └── convos/              # История диалогов (автоматически)
└── setup.sh                  # Скрипт инициализации
```

---

## ❓ FAQ

**Q: Где взять SSH данные?**  
A: В панели Timeweb → Ваше приложение → раздел SSH/Терминал

**Q: Можно ли редактировать файлы без SSH?**  
A: Да, через файловый менеджер в веб-интерфейсе Timeweb

**Q: Как загрузить много файлов сразу?**  
A: Используйте SFTP клиент (FileZilla, WinSCP) или команду `scp`

**Q: Worker не запускается!**  
A: Проверьте:
1. Установлен ли `OPENAI_API_KEY` в ENV
2. Есть ли файл `config.json`
3. Загружены ли `.session` файлы в `data/sessions/`
4. Посмотрите логи в панели Timeweb

**Q: Где посмотреть логи?**  
A: В панели Timeweb → Ваше приложение → вкладка "Логи" или "Logs"

