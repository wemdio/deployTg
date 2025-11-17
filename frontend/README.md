# Telegram Auto-Responder - Frontend

React веб-интерфейс для управления Telegram кампаниями.

## Требования

- Node.js 16+
- npm или yarn

## Установка зависимостей

```bash
npm install
```

## Запуск

### Разработка
```bash
npm start
```

Откроется в браузере на `http://localhost:3000`

### Сборка для продакшена
```bash
npm run build
```

Результат сборки будет в папке `build/`

## Конфигурация

Frontend подключается к backend API. 
Для локальной разработки используется proxy (настроен в `src/setupProxy.js`).

В production режиме frontend должен обслуживаться через nginx и проксировать API запросы к backend.

## Структура

- `src/components/` - React компоненты
- `src/api/` - Клиент для API запросов
- `public/` - Статические файлы

## Особенности для Timeweb

При деплое на Timeweb Cloud:
- Тип приложения: **frontend**
- Фреймворк: **react**
- Команда сборки: `npm run build`
- Директория с index файлом: `build`

