# 🚀 Деплой на Timeweb Cloud

Полная инструкция по развертыванию TG Auto-Responder на Timeweb Cloud.

---

## 📋 Требования

- ✅ Аккаунт Timeweb Cloud
- ✅ GitHub репозиторий (публичный или приватный)
- ✅ API токен Timeweb (для MCP)

---

## 🏗️ Архитектура приложения

Приложение состоит из **ДВУХ** компонентов, которые работают вместе:

### 1️⃣ **Backend (FastAPI)** - задеплоен на Timeweb ✅
- REST API для управления кампаниями
- Управление Telegram аккаунтами
- **Запускает и управляет Worker процессами**

### 2️⃣ **Worker (Telegram Bot)** - запускается Backend'ом
- Подключается к Telegram
- Отвечает на сообщения через OpenAI
- Работает в background процессе

---

## 🎯 Вариант 1: Деплой Backend (Рекомендуется)

### **Шаг 1: Подготовка репозитория**

```bash
# Коммитим все изменения
git add .
git commit -m "feat: integrate worker into backend"
git push origin main  # или ваша ветка
```

### **Шаг 2: Создание приложения на Timeweb**

1. Откройте: https://timeweb.cloud/my/applications
2. Нажмите **"Создать приложение"**
3. Выберите **VCS provider** (GitHub)
4. Выберите ваш репозиторий

### **Шаг 3: Настройки деплоя**

```yaml
Тип приложения:     Backend
Фреймворк:          FastAPI
Окружение:          Python
Версия:             3.12

Ветка:              main  # или ваша ветка

Команда сборки:     pip install --no-cache-dir -r backend/requirements.txt

Команда запуска:    bash backend/start.sh

Рабочая директория: /app
```

### **Шаг 4: Переменные окружения (ВАЖНО! 🔐)**

Добавьте в разделе **"Переменные"**:

```bash
# OpenAI (обязательно!)
OPENAI_API_KEY=sk-proj-ваш_ключ_здесь

# Опционально: прокси для OpenAI
OPENAI_PROXY=http://user:pass@host:port
```

### **Шаг 5: Деплой**

1. Нажмите **"Создать"**
2. Дождитесь окончания сборки (~5-10 минут)
3. Проверьте логи на наличие ошибок

### **Шаг 6: Проверка**

Откройте в браузере:
```
https://ваш-домен.twc1.net/health
```

Должны увидеть:
```json
{
  "status": "healthy",
  "running_campaigns": 0,
  "total_campaigns": 0
}
```

API документация доступна на:
```
https://ваш-домен.twc1.net/docs
```

---

## 🎨 Вариант 2: Деплой Frontend (опционально)

Если вы хотите веб-интерфейс для управления:

### **Настройки деплоя Frontend:**

```yaml
Тип приложения:        Frontend
Фреймворк:             React
Окружение:             Node.js
Версия:                18

Ветка:                 main

Команда сборки:        npm install && npm run build

Директория с index:    frontend/build

Команда запуска:       npm start
```

### **Переменные окружения для Frontend:**

```bash
REACT_APP_API_URL=https://ваш-backend-домен.twc1.net
```

---

## 🔧 Настройка после деплоя

### 1. Обновить URL в Frontend (если нужно)

Откройте `src/api/client.js`:

```javascript
const API_URL = process.env.REACT_APP_API_URL || 
                (process.env.NODE_ENV === 'production' 
                  ? 'https://ваш-реальный-backend.twc1.net'  // ← ИЗМЕНИТЬ
                  : 'http://localhost:8000');
```

### 2. Создать первую кампанию

Через API или веб-интерфейс:

1. Создайте кампанию
2. Добавьте OpenAI ключ в настройки
3. Загрузите Telegram сессии
4. Запустите кампанию

---

## 📁 Структура файлов на Timeweb

После деплоя на сервере будет:

```
/app/
├── backend/
│   ├── app/
│   │   ├── main.py              ← FastAPI приложение
│   │   ├── campaign_manager.py  ← Управление процессами
│   │   └── api/                 ← API роутеры
│   ├── campaigns/               ← Конфиги кампаний (сохраняются!)
│   ├── campaigns_runtime/       ← Worker процессы (сохраняются!)
│   └── data/
│       └── sessions/            ← Telegram сессии (сохраняются!)
```

**Важно:** Все данные в этих папках **сохраняются** между деплоями!

---

## 💾 Сохранность данных

### ✅ Что сохраняется между деплоями:

- ✅ Конфигурации кампаний (`backend/campaigns/`)
- ✅ Telegram сессии (`backend/data/sessions/`)
- ✅ История диалогов (`backend/campaigns_runtime/*/data/convos/`)
- ✅ Списки обработанных клиентов (`processed_clients.txt`)
- ✅ Логи (`errors.log`)

### ❌ Что НЕ сохраняется:

- ❌ Запущенные процессы (worker перезапустится автоматически)
- ❌ RAM данные (кеш в памяти)

---

## 🔐 Безопасность

### ⚠️ **КРИТИЧЕСКИ ВАЖНО!**

**НЕ ХРАНИТЕ секреты в репозитории!**

### ❌ **Плохо:**
```json
{
  "OPENAI": {
    "API_KEY": "sk-proj-реальный-ключ"  // ← УТЕЧКА!
  }
}
```

### ✅ **Хорошо:**
```python
import os

api_key = os.getenv("OPENAI_API_KEY")  # Из переменных окружения
```

### 🛡️ **Защита секретов:**

1. **Добавить в `.gitignore`:**
   ```gitignore
   config.json
   *.session
   api_map.txt
   proxies.txt
   .env
   ```

2. **Использовать переменные окружения Timeweb**
3. **Регулярно ротировать токены**

### 🔒 **Отозвать скомпрометированные ключи:**

Если вы случайно закоммитили секреты:

1. **OpenAI:** https://platform.openai.com/api-keys → Удалить ключ
2. **GitHub:** Создать новый Personal Access Token
3. **Прокси:** Сменить пароль

---

## 🐛 Troubleshooting

### Проблема: Backend не запускается

**Проверьте логи:**
```
Timeweb Dashboard → Ваше приложение → Логи приложения
```

**Частые ошибки:**

1. **ModuleNotFoundError**
   - Решение: Проверьте `requirements.txt`
   - Добавьте недостающий пакет

2. **Permission denied**
   - Решение: `chmod +x backend/start.sh`

3. **Port already in use**
   - Решение: Timeweb автоматически назначает порт

### Проблема: Кампания не запускается

**Причины:**
- ❌ Нет аккаунтов
- ❌ Нет OpenAI ключа
- ❌ Невалидные сессии Telegram

**Решение:**
```bash
# Проверьте через API:
curl https://ваш-домен.twc1.net/campaigns/{id}/logs
```

### Проблема: Worker падает с ошибкой

**Проверьте логи кампании:**
```
backend/campaigns_runtime/{campaign_id}/errors.log
```

**Частые проблемы:**
- `OperationalError: unable to open database` - неправильные пути к сессиям
- `AuthKeyUnregisteredError` - сессия устарела
- `FloodWaitError` - Telegram ограничил действия

---

## 📊 Мониторинг

### Health Check

```bash
curl https://ваш-домен.twc1.net/health
```

### Статистика кампании

```bash
curl https://ваш-домен.twc1.net/campaigns/{id}/stats
```

### Логи кампании

```bash
curl https://ваш-домен.twc1.net/campaigns/{id}/logs?limit=50
```

---

## 🔄 Обновление приложения

### Автоматический деплой (рекомендуется)

1. Пушите изменения в GitHub:
   ```bash
   git add .
   git commit -m "feat: новая фича"
   git push
   ```

2. Timeweb автоматически задеплоит изменения

### Ручной деплой

В Timeweb Dashboard:
1. Приложения → Ваше приложение
2. Нажать **"Передеплоить"**

---

## 🎓 Полезные команды

### Проверка статуса через API

```bash
# Список кампаний
curl https://ваш-домен.twc1.net/campaigns/

# Запустить кампанию
curl -X POST https://ваш-домен.twc1.net/campaigns/{id}/start

# Остановить кампанию
curl -X POST https://ваш-домен.twc1.net/campaigns/{id}/stop

# Загрузить сессию
curl -X POST -F "session_file=@194453263.session" \
  https://ваш-домен.twc1.net/accounts/{campaign_id}/upload-session
```

---

## 📚 Дополнительная информация

- 📖 **API Документация:** `https://ваш-домен.twc1.net/docs`
- 🔧 **Timeweb Cloud:** https://timeweb.cloud/
- 💬 **Поддержка Timeweb:** https://timeweb.cloud/help

---

## ✅ Checklist деплоя

- [ ] Репозиторий на GitHub создан
- [ ] `.gitignore` настроен (нет секретов в Git)
- [ ] Backend код закоммичен
- [ ] Приложение создано на Timeweb
- [ ] Переменные окружения добавлены
- [ ] Backend задеплоен и работает (`/health` отвечает)
- [ ] API документация доступна (`/docs`)
- [ ] Frontend настроен на правильный API URL (если используется)
- [ ] Первая кампания создана и тестируется

---

**Готово! Ваше приложение задеплоено на Timeweb Cloud! 🎉**

