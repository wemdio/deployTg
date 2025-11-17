#!/bin/bash
# Скрипт инициализации для Timeweb Cloud Worker

echo "🔧 Настройка Telegram Auto-Responder Worker..."

# Создаем необходимые директории
mkdir -p data/sessions
mkdir -p data/convos

# Создаем config.json из примера если его нет
if [ ! -f "config.json" ]; then
    echo "📝 Создание config.json..."
    cp config.example.json config.json
    
    # Если есть ENV переменная OPENAI_API_KEY, используем её
    if [ ! -z "$OPENAI_API_KEY" ]; then
        echo "✅ Найден OPENAI_API_KEY в переменных окружения"
        # Обновляем config.json с ключом из ENV
        sed -i "s/sk-your-openai-api-key-here/$OPENAI_API_KEY/g" config.json
    else
        echo "⚠️  OPENAI_API_KEY не найден в переменных окружения!"
        echo "   Добавьте его в панели Timeweb или отредактируйте config.json вручную"
    fi
fi

# Создаем prompt.txt из примера если его нет
if [ ! -f "prompt.txt" ]; then
    echo "📝 Создание prompt.txt..."
    cp prompt.example.txt prompt.txt
fi

# Создаем пустые файлы для обработанных пользователей
touch processed_clients.txt

echo "✅ Инициализация завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Отредактируйте config.json (укажите TARGET_CHATS, PROJECT_NAME)"
echo "2. Отредактируйте prompt.txt (настройте системный промпт)"
echo "3. Загрузите Telegram сессии в data/sessions/"
echo "4. Создайте api_map.txt если используете несколько аккаунтов"
echo ""
echo "🚀 Запуск: python main.py"

