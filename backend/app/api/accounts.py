"""
Accounts API Router
Управление Telegram аккаунтами
"""
import os
import shutil
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

from ..campaign_manager import campaign_manager


router = APIRouter()


class AccountCreate(BaseModel):
    session_name: str
    api_id: int
    api_hash: str
    proxy: Optional[str] = None


# ============================================
# СПЕЦИФИЧНЫЕ МАРШРУТЫ (БЕЗ ПАРАМЕТРОВ) - ДОЛЖНЫ БЫТЬ ПЕРВЫМИ!
# ============================================

@router.get("/available")
async def get_available_sessions():
    """Получить список доступных сессий"""
    sessions_dir = Path("backend/data/sessions")
    if not sessions_dir.exists():
        return []
    
    sessions = []
    for file in sessions_dir.glob("*.session"):
        session_name = file.stem
        json_file = sessions_dir / f"{session_name}.json"
        
        has_json = json_file.exists()
        
        sessions.append({
            "session_name": session_name,
            "has_credentials": has_json,
            "file_path": str(file)
        })
    
    return sessions


# ============================================
# ПАРАМЕТРИЧЕСКИЕ МАРШРУТЫ (С {campaign_id})
# ============================================

@router.get("/{campaign_id}")
async def get_campaign_accounts(campaign_id: str):
    """Получить список аккаунтов кампании"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return campaign.get("accounts", [])


@router.post("/{campaign_id}")
async def add_account(campaign_id: str, account: AccountCreate):
    """Добавить аккаунт в кампанию"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Проверяем не существует ли уже
    existing = [a for a in campaign.get("accounts", []) if a["session_name"] == account.session_name]
    if existing:
        raise HTTPException(status_code=400, detail="Account with this session name already exists")
    
    # Добавляем аккаунт
    if "accounts" not in campaign:
        campaign["accounts"] = []
    
    campaign["accounts"].append(account.dict())
    campaign_manager.save_campaign(campaign)
    
    return account.dict()


@router.put("/{campaign_id}/{session_name}")
async def update_account(campaign_id: str, session_name: str, account: AccountCreate):
    """Обновить аккаунт"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Находим аккаунт
    accounts = campaign.get("accounts", [])
    account_index = None
    for i, acc in enumerate(accounts):
        if acc["session_name"] == session_name:
            account_index = i
            break
    
    if account_index is None:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Обновляем
    accounts[account_index] = account.dict()
    campaign_manager.save_campaign(campaign)
    
    return account.dict()


@router.delete("/{campaign_id}/{session_name}")
async def delete_account(campaign_id: str, session_name: str):
    """Удалить аккаунт из кампании"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Находим и удаляем аккаунт
    accounts = campaign.get("accounts", [])
    initial_len = len(accounts)
    accounts = [a for a in accounts if a["session_name"] != session_name]
    
    if len(accounts) == initial_len:
        raise HTTPException(status_code=404, detail="Account not found")
    
    campaign["accounts"] = accounts
    campaign_manager.save_campaign(campaign)
    
    # Удаляем файлы сессии
    session_path = Path(f"backend/data/sessions/{session_name}.session")
    json_path = Path(f"backend/data/sessions/{session_name}.json")
    
    if session_path.exists():
        session_path.unlink()
    if json_path.exists():
        json_path.unlink()
    
    return {"message": "Account deleted", "session_name": session_name}


@router.post("/{campaign_id}/upload-session")
async def upload_session(
    campaign_id: str,
    session_file: UploadFile = File(...),
    session_name: Optional[str] = Form(None)
):
    """Загрузить .session файл"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Проверяем расширение
    if not session_file.filename.endswith(".session"):
        raise HTTPException(status_code=400, detail="File must be a .session file")
    
    # Определяем имя сессии
    if not session_name:
        session_name = session_file.filename.replace(".session", "")
    
    # Создаем папку если нужно
    sessions_dir = Path("backend/data/sessions")
    sessions_dir.mkdir(parents=True, exist_ok=True)
    
    # Сохраняем файл
    file_path = sessions_dir / f"{session_name}.session"
    with open(file_path, "wb") as f:
        content = await session_file.read()
        f.write(content)
    
    return {
        "message": "Session file uploaded",
        "session_name": session_name,
        "file_path": str(file_path)
    }


@router.post("/{campaign_id}/upload-json")
async def upload_json(
    campaign_id: str,
    json_file: UploadFile = File(...)
):
    """Загрузить .json файл с credentials"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Проверяем расширение
    if not json_file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="File must be a .json file")
    
    import json
    
    # Читаем JSON
    content = await json_file.read()
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON file: {str(e)}")
    
    # Извлекаем данные - поддерживаем разные форматы
    session_name = json_file.filename.replace(".json", "")
    
    # Пробуем разные варианты ключей
    api_id = (
        data.get("app_id") or 
        data.get("api_id") or 
        data.get("APP_ID") or
        data.get("API_ID")
    )
    
    api_hash = (
        data.get("app_hash") or 
        data.get("api_hash") or
        data.get("APP_HASH") or
        data.get("API_HASH")
    )
    
    proxy = data.get("proxy") or data.get("PROXY")
    
    # Логируем для отладки
    print(f"📋 Parsing JSON for {session_name}")
    print(f"   Keys in JSON: {list(data.keys())}")
    print(f"   api_id: {api_id}, api_hash: {'present' if api_hash else 'missing'}")
    
    if not api_id or not api_hash:
        raise HTTPException(
            status_code=400, 
            detail=f"JSON must contain api_id and api_hash. Found keys: {list(data.keys())}"
        )
    
    # Сохраняем JSON файл
    sessions_dir = Path("backend/data/sessions")
    sessions_dir.mkdir(parents=True, exist_ok=True)
    
    json_path = sessions_dir / f"{session_name}.json"
    with open(json_path, "wb") as f:
        f.write(content)
    
    # Добавляем аккаунт в кампанию
    account = AccountCreate(
        session_name=session_name,
        api_id=int(api_id),
        api_hash=api_hash,
        proxy=proxy if proxy and proxy != "null" else None
    )
    
    # Проверяем не существует ли уже
    existing = [a for a in campaign.get("accounts", []) if a["session_name"] == session_name]
    if not existing:
        if "accounts" not in campaign:
            campaign["accounts"] = []
        campaign["accounts"].append(account.dict())
        campaign_manager.save_campaign(campaign)
    
    return {
        "message": "JSON file uploaded and account added",
        "session_name": session_name,
        "account": account.dict()
    }
