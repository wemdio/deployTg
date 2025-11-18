# 👨‍💻 Настройка для разработчиков

Инструкция для новых разработчиков в команде.

---

## 🚀 Быстрый старт

### 1️⃣ **Клонирование репозитория**

```bash
# HTTPS (потребуется GitHub токен)
git clone https://github.com/wemdio/deployTg.git
cd deployTg

# Или SSH (если настроен)
git clone git@github.com:wemdio/deployTg.git
cd deployTg
```

### 2️⃣ **Переключиться на рабочую ветку**

```bash
git checkout frontend
```

### 3️⃣ **Установка зависимостей**

#### **Backend (Python)**

```bash
cd backend
pip install -r requirements.txt
cd ..
```

#### **Frontend (Node.js)**

```bash
cd frontend
npm install
cd ..
```

---

## 💻 Локальная разработка

### **Запустить всё сразу:**

```bash
# Windows
start_all_local.bat

# Или вручную в двух терминалах:
```

**Терминал 1 - Backend:**
```bash
start_backend_local.bat
# Или: cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Терминал 2 - Frontend:**
```bash
start_frontend_local.bat
# Или: cd frontend && npm start
```

### **Откроется:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📝 Работа с Git

### **Базовый workflow:**

```bash
# 1. Убедиться что на актуальной ветке
git checkout frontend
git pull origin frontend

# 2. Создать feature ветку (опционально)
git checkout -b feature/my-new-feature

# 3. Внести изменения
# ... редактируем файлы ...

# 4. Посмотреть что изменилось
git status

# 5. Добавить изменения
git add .
# Или конкретные файлы:
git add backend/app/main.py frontend/src/App.js

# 6. Закоммитить
git commit -m "feat: описание изменений"

# 7. Запушить
git push origin frontend
# Или в feature ветку:
git push origin feature/my-new-feature
```

### **Формат коммитов (рекомендуется):**

```
feat: добавлена новая фича
fix: исправлен баг
docs: обновлена документация
refactor: рефакторинг кода
style: форматирование
test: добавлены тесты
chore: обновлены зависимости
```

---

## 🔐 GitHub аутентификация

### **Вариант 1: HTTPS + Personal Access Token**

1. Создать токен: https://github.com/settings/tokens
2. Права: `repo`
3. При `git push` использовать токен вместо пароля

### **Вариант 2: SSH ключ (рекомендуется)**

```bash
# Генерация SSH ключа
ssh-keygen -t ed25519 -C "your_email@example.com"

# Добавить в GitHub
# https://github.com/settings/keys
cat ~/.ssh/id_ed25519.pub  # скопировать и вставить

# Использовать SSH URL
git remote set-url origin git@github.com:wemdio/deployTg.git
```

---

## 📂 Структура проекта

```
tgrespNadeploy/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py      # Основной файл
│   │   ├── campaign_manager.py
│   │   └── api/         # API роутеры
│   └── requirements.txt
│
├── frontend/            # React frontend  
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   └── api/client.js
│   └── package.json
│
├── campaigns_runtime/   # Worker шаблон
│   └── .../main.py     # Telethon worker
│
├── .gitignore          # Защита секретов
├── README.md           # Главная документация
├── DEPLOY_TIMEWEB.md   # Деплой инструкции
└── LOCAL_DEVELOPMENT.md # Локальная разработка
```

---

## 🔧 Настройка IDE

### **VS Code (рекомендуется)**

Расширения:
- Python
- Pylance
- ES7+ React/Redux/React-Native snippets
- GitLens
- ESLint
- Prettier

### **PyCharm / WebStorm**

Настроить интерпретатор Python и Node.js.

---

## 🐛 Решение проблем

### **Backend не запускается**

```bash
# Проверить Python версию (нужен 3.10+)
python --version

# Переустановить зависимости
cd backend
pip install --no-cache-dir -r requirements.txt
```

### **Frontend не запускается**

```bash
# Проверить Node версию (нужен 16+)
node --version

# Очистить и переустановить
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### **Git push не работает**

```bash
# Проверить права доступа
git remote -v

# Проверить что вы добавлены как collaborator
# Спросить у владельца репозитория
```

---

## 🚀 Деплой на Timeweb

После внесения изменений и пуша в GitHub:

1. Timeweb автоматически подхватит изменения
2. Или вручную: Timeweb Dashboard → Приложение → **Передеплоить**

Подробнее: [DEPLOY_TIMEWEB.md](DEPLOY_TIMEWEB.md)

---

## 📚 Полезные команды

### **Backend:**

```bash
# Запуск с hot-reload
cd backend
uvicorn app.main:app --reload

# Проверка зависимостей
pip list

# Добавить новую зависимость
pip install package_name
pip freeze > requirements.txt
```

### **Frontend:**

```bash
# Запуск dev сервера
cd frontend
npm start

# Сборка для production
npm run build

# Добавить новую зависимость
npm install package_name
```

### **Git:**

```bash
# Посмотреть историю
git log --oneline -10

# Отменить последний коммит (не запушенный)
git reset --soft HEAD~1

# Синхронизироваться с remote
git pull --rebase origin frontend

# Посмотреть изменения
git diff
```

---

## ✅ Checklist первого запуска

- [ ] Репозиторий склонирован
- [ ] Ветка `frontend` активна
- [ ] Python 3.10+ установлен
- [ ] Node.js 16+ установлен
- [ ] Backend зависимости установлены (`pip install -r backend/requirements.txt`)
- [ ] Frontend зависимости установлены (`cd frontend && npm install`)
- [ ] Backend запускается (http://localhost:8000)
- [ ] Frontend запускается (http://localhost:3000)
- [ ] Git настроен (имя, email, SSH/токен)
- [ ] Доступ к GitHub репозиторию есть
- [ ] Первый тестовый коммит и push работает

---

## 🆘 Помощь

Если что-то не работает:
1. Проверьте версии Python и Node.js
2. Прочитайте [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md)
3. Проверьте логи в консоли
4. Спросите в команде

---

**Добро пожаловать в команду! 🎉**

