# 📤 Что передать другу для работы над проектом

---

## ✅ Чеклист передачи

### 1️⃣ **GitHub доступ**

**Действия владельца (вы):**
1. Открыть: https://github.com/wemdio/deployTg/settings/access
2. Нажать **"Add people"**
3. Ввести GitHub username друга
4. Выбрать права: **Write** (или **Admin** если нужен полный доступ)
5. Друг получит email приглашение

**Передать другу:**
- ✅ URL репозитория: `https://github.com/wemdio/deployTg.git`
- ✅ Рабочая ветка: `frontend`
- ✅ Этот файл: [SETUP_FOR_DEVELOPERS.md](SETUP_FOR_DEVELOPERS.md)

---

### 2️⃣ **Timeweb Cloud доступ**

**Действия владельца (вы):**
1. Открыть: https://timeweb.cloud/
2. Настройки → Пользователи → Добавить
3. Или передать учётные данные

**Что передать:**
- ✅ Учётные данные Timeweb (логин/пароль)
- ✅ Ссылка на приложения:
  - Backend: https://wemdio-deploytg-1e6b.twc1.net
  - Frontend: https://wemdio-deploytg-9cca.twc1.net

---

### 3️⃣ **Документация**

**Передать файлы:**
- ✅ [SETUP_FOR_DEVELOPERS.md](SETUP_FOR_DEVELOPERS.md) - настройка окружения
- ✅ [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md) - локальная разработка
- ✅ [DEPLOY_TIMEWEB.md](DEPLOY_TIMEWEB.md) - деплой на Timeweb
- ✅ [README.md](README.md) - общая документация

---

### 4️⃣ **Требования к системе**

**Друг должен установить:**
- ✅ Python 3.10+ (https://www.python.org/downloads/)
- ✅ Node.js 16+ (https://nodejs.org/)
- ✅ Git (https://git-scm.com/)
- ✅ VS Code или другой редактор

---

## 📧 Шаблон письма другу

```
Привет!

Добавил тебя в проект TG Auto-Responder.

🔗 Репозиторий: https://github.com/wemdio/deployTg
🌿 Ветка: frontend

📋 Что делать:
1. Прими приглашение на GitHub (придёт на email)
2. Склонируй репозиторий
3. Прочитай SETUP_FOR_DEVELOPERS.md
4. Настрой локальное окружение
5. Запусти и протестируй

🌐 Timeweb доступ:
Логин: [ваш_логин]
Пароль: [ваш_пароль]

Backend: https://wemdio-deploytg-1e6b.twc1.net
Frontend: https://wemdio-deploytg-9cca.twc1.net

Если что-то не работает - пиши!
```

---

## 🔐 Безопасность

### ⚠️ **НЕ передавайте в Git:**
- ❌ OpenAI API ключи
- ❌ Telegram сессии (*.session)
- ❌ Файлы с паролями (api_map.txt, proxies.txt)
- ❌ Конфиги с секретами (config.json с ключами)

Всё это защищено `.gitignore` - но следите чтобы случайно не закоммитить!

### ✅ **Безопасная передача секретов:**
Если нужно передать тестовые ключи/сессии:
- Использовать защищённые каналы (не email!)
- Telegram Secret Chat
- Signal
- Зашифрованный архив с паролем

---

## 🎯 Первые задачи для друга

После настройки окружения:

1. ✅ Запустить локально (backend + frontend)
2. ✅ Создать тестовую кампанию в UI
3. ✅ Сделать тестовое изменение (например, в README)
4. ✅ Закоммитить и запушить
5. ✅ Проверить что изменения появились на GitHub

---

## 📞 Контакты для помощи

Если у друга проблемы:
1. Проверить [SETUP_FOR_DEVELOPERS.md](SETUP_FOR_DEVELOPERS.md)
2. Проверить версии Python и Node.js
3. Написать вам
4. Создать Issue на GitHub

---

## ✅ Финальный чеклист передачи

- [ ] Добавлен как Collaborator на GitHub
- [ ] Передан URL репозитория
- [ ] Передана ветка для работы (frontend)
- [ ] Передан доступ к Timeweb
- [ ] Передана документация (SETUP_FOR_DEVELOPERS.md и др.)
- [ ] Объяснены требования к системе
- [ ] Друг принял приглашение на GitHub
- [ ] Друг успешно склонировал репозиторий
- [ ] Друг запустил проект локально
- [ ] Друг сделал тестовый коммит

---

**Готово! Теперь можете работать вместе! 🤝**

