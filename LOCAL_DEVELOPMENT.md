# 💻 Локальная разработка

## 🚀 Быстрый старт

### Вариант 1: Запустить всё сразу (Рекомендуется)

Просто **дважды кликните** на файл:
```
start_all_local.bat
```

Это откроет 2 окна:
- ✅ Backend API на `http://localhost:8000`
- ✅ Frontend на `http://localhost:3000` (откроется в браузере автоматически)

### Вариант 2: Запустить по отдельности

**Backend только:**
```
start_backend_local.bat
```

**Frontend только:**
```
start_frontend_local.bat
```

---

## 📋 Что запускается?

### Backend (FastAPI)
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Порт**: 8000

**Что делает:**
- API для управления кампаниями
- CRUD операции с аккаунтами
- WebSocket для real-time обновлений

### Frontend (React)
- **URL**: http://localhost:3000
- **Порт**: 3000

**Что делает:**
- Веб-интерфейс для управления
- Подключается к Backend API через proxy
- Real-time обновления через WebSocket

---

## 🔧 Требования

### Для Backend:
- ✅ Python 3.10+ ([Скачать](https://www.python.org/downloads/))
- ✅ pip (устанавливается с Python)

### Для Frontend:
- ✅ Node.js 16+ ([Скачать](https://nodejs.org/))
- ✅ npm (устанавливается с Node.js)

---

## 📁 Структура проекта

```
tgrespNadeploy/
├── backend/                    # FastAPI приложение
│   ├── app/
│   │   ├── main.py            # Основной файл приложения
│   │   ├── api/               # API роутеры
│   │   ├── models.py          # Pydantic модели
│   │   ├── database.py        # Работа с JSON БД
│   │   └── campaign_manager.py # Управление кампаниями
│   ├── requirements.txt       # Python зависимости
│   └── run.py                 # Точка входа
│
├── frontend/                   # React приложение
│   ├── src/
│   │   ├── App.js             # Главный компонент
│   │   ├── components/        # React компоненты
│   │   ├── api/client.js      # API клиент
│   │   └── setupProxy.js      # Proxy для development
│   ├── public/
│   └── package.json           # npm зависимости
│
├── main.py                     # Worker (отдельное приложение)
├── config.json                 # Конфигурация worker
│
├── start_all_local.bat        # Запустить всё
├── start_backend_local.bat    # Запустить только backend
└── start_frontend_local.bat   # Запустить только frontend
```

---

## 🐛 Решение проблем

### Backend не запускается

**Ошибка:** `python: command not found`

**Решение:**
1. Установите Python: https://www.python.org/downloads/
2. При установке отметьте "Add Python to PATH"
3. Перезагрузите терминал

**Ошибка:** `No module named 'fastapi'`

**Решение:**
```bash
cd backend
pip install -r requirements.txt
```

### Frontend не запускается

**Ошибка:** `npm: command not found`

**Решение:**
1. Установите Node.js: https://nodejs.org/
2. Перезагрузите терминал

**Ошибка:** `Cannot find module`

**Решение:**
```bash
cd frontend
npm install
```

### Frontend не подключается к Backend

**Проблема:** CORS ошибки или "Network Error"

**Решение:**
1. Убедитесь что Backend запущен на порту 8000
2. Проверьте `frontend/src/setupProxy.js` - там настроен proxy на `http://localhost:8000`
3. Перезапустите оба приложения

### Порт уже занят

**Ошибка:** `Port 8000 is already in use`

**Решение:**
- Закройте другое приложение использующее этот порт
- Или измените порт в `backend/run.py`:
  ```python
  uvicorn.run(..., port=8001)  # Измените на свободный порт
  ```

---

## 🔨 Команды для разработки

### Backend

```bash
cd backend

# Установить зависимости
pip install -r requirements.txt

# Запустить с hot-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Запустить тесты (если есть)
pytest

# Проверить типы
mypy app/
```

### Frontend

```bash
cd frontend

# Установить зависимости
npm install

# Запустить dev сервер
npm start

# Собрать для продакшена
npm run build

# Запустить тесты
npm test

# Проверить код
npm run lint
```

---

## 🌐 API Endpoints

После запуска backend доступен по адресу `http://localhost:8000`

### Основные эндпоинты:

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/` | Информация об API |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Swagger UI документация |
| `GET` | `/redoc` | ReDoc документация |
| `GET` | `/api/campaigns` | Список кампаний |
| `POST` | `/api/campaigns` | Создать кампанию |
| `GET` | `/api/campaigns/{id}` | Получить кампанию |
| `PUT` | `/api/campaigns/{id}` | Обновить кампанию |
| `DELETE` | `/api/campaigns/{id}` | Удалить кампанию |
| `GET` | `/api/accounts` | Список аккаунтов |
| `POST` | `/api/accounts` | Добавить аккаунт |
| `WebSocket` | `/ws` | Real-time обновления |

---

## 📝 Примечания

### Proxy для Frontend

Frontend использует proxy для обхода CORS в development режиме.  
Настроен в `frontend/src/setupProxy.js`:

```javascript
module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:8000',
      changeOrigin: true,
    })
  );
};
```

Это означает что запросы к `/api/*` автоматически проксируются на Backend.

### Hot Reload

- **Backend**: Изменения в коде требуют ручного перезапуска
- **Frontend**: Изменения применяются автоматически (Hot Module Replacement)

### База данных

Backend использует JSON файлы для хранения данных:
- `backend/campaigns/*.json` - конфигурации кампаний
- Данные хранятся локально, без внешней БД

---

## ✅ Checklist перед началом работы

- [ ] Python 3.10+ установлен
- [ ] Node.js 16+ установлен
- [ ] Зависимости backend установлены (`pip install -r requirements.txt`)
- [ ] Зависимости frontend установлены (`npm install`)
- [ ] Порты 8000 и 3000 свободны
- [ ] Backend запущен и доступен
- [ ] Frontend запущен и открывается в браузере

---

## 🎯 Следующие шаги

После запуска локально:
1. Откройте http://localhost:3000
2. Создайте тестовую кампанию
3. Добавьте аккаунт
4. Протестируйте функционал

Для деплоя на Timeweb смотрите основной README.md

---

**Удачной разработки!** 🚀


