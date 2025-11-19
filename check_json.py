#!/usr/bin/env python3
"""
Скрипт для проверки формата JSON файлов аккаунтов
"""
import json
import sys

if len(sys.argv) < 2:
    print("Usage: python check_json.py <path_to_json_file>")
    print("Example: python check_json.py 194453263.json")
    sys.exit(1)

json_file = sys.argv[1]

try:
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ JSON файл корректен: {json_file}")
    print(f"\n📋 Структура JSON:")
    print(f"   Ключи: {list(data.keys())}")
    print(f"\n📊 Полные данные:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    # Проверяем наличие необходимых полей
    print(f"\n🔍 Проверка полей:")
    
    api_id_keys = ["app_id", "api_id", "APP_ID", "API_ID", "appId", "apiId"]
    api_hash_keys = ["app_hash", "api_hash", "APP_HASH", "API_HASH", "appHash", "apiHash"]
    
    found_api_id = None
    for key in api_id_keys:
        if key in data:
            found_api_id = (key, data[key])
            print(f"   ✅ api_id найден: '{key}' = {data[key]}")
            break
    
    if not found_api_id:
        print(f"   ❌ api_id НЕ найден! Искали ключи: {api_id_keys}")
    
    found_api_hash = None
    for key in api_hash_keys:
        if key in data:
            found_api_hash = (key, data[key])
            print(f"   ✅ api_hash найден: '{key}' = {'***' * 5}")
            break
    
    if not found_api_hash:
        print(f"   ❌ api_hash НЕ найден! Искали ключи: {api_hash_keys}")
    
    if "proxy" in data or "PROXY" in data:
        proxy = data.get("proxy") or data.get("PROXY")
        print(f"   ✅ proxy найден: {proxy}")
    else:
        print(f"   ⚠️ proxy не найден (необязательное поле)")

except FileNotFoundError:
    print(f"❌ Файл не найден: {json_file}")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"❌ Ошибка парсинга JSON: {e}")
    sys.exit(1)

