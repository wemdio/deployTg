"""
Dialogs API Router
Управление диалогами и историей
"""
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

from ..campaign_manager import campaign_manager


router = APIRouter()


@router.get("/{campaign_id}")
async def get_campaign_dialogs(campaign_id: str):
    """Получить список диалогов кампании"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    runtime_path = Path(f"backend/campaigns_runtime/{campaign_id}")
    convos_dir = runtime_path / "data" / "convos"
    
    if not convos_dir.exists():
        return []
    
    dialogs = []
    for file in convos_dir.glob("*.jsonl"):
        # Парсим имя файла: sessionname_userid_username.jsonl
        parts = file.stem.split("_")
        if len(parts) >= 2:
            session_name = parts[0]
            user_id = parts[1]
            username = "_".join(parts[2:]) if len(parts) > 2 else None
            
            # Считаем количество сообщений
            with open(file, "r", encoding="utf-8") as f:
                messages_count = len([line for line in f if line.strip()])
            
            dialogs.append({
                "session_name": session_name,
                "user_id": user_id,
                "username": username,
                "messages_count": messages_count,
                "file_path": str(file)
            })
    
    return dialogs


@router.get("/{campaign_id}/{session_name}/{user_id}")
async def get_dialog(campaign_id: str, session_name: str, user_id: str):
    """Получить историю конкретного диалога"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    runtime_path = Path(f"backend/campaigns_runtime/{campaign_id}")
    convos_dir = runtime_path / "data" / "convos"
    
    # Ищем файл диалога (может быть с username или без)
    dialog_file = None
    for file in convos_dir.glob(f"{session_name}_{user_id}*.jsonl"):
        dialog_file = file
        break
    
    if not dialog_file or not dialog_file.exists():
        raise HTTPException(status_code=404, detail="Dialog not found")
    
    # Читаем сообщения
    messages = []
    with open(dialog_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    messages.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    
    return {
        "session_name": session_name,
        "user_id": user_id,
        "messages": messages,
        "total": len(messages)
    }


@router.delete("/{campaign_id}/{session_name}/{user_id}")
async def delete_dialog(campaign_id: str, session_name: str, user_id: str):
    """Удалить историю диалога"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    runtime_path = Path(f"backend/campaigns_runtime/{campaign_id}")
    convos_dir = runtime_path / "data" / "convos"
    
    # Ищем и удаляем файл диалога
    deleted = False
    for file in convos_dir.glob(f"{session_name}_{user_id}*.jsonl"):
        file.unlink()
        deleted = True
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Dialog not found")
    
    return {"message": "Dialog deleted"}


@router.get("/{campaign_id}/processed")
async def get_processed_clients(campaign_id: str):
    """Получить список обработанных клиентов"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    runtime_path = Path(f"backend/campaigns_runtime/{campaign_id}")
    processed_file = runtime_path / "processed_clients.txt"
    
    if not processed_file.exists():
        return []
    
    clients = []
    with open(processed_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                # Формат: "user_id | @username"
                parts = line.split("|", 1)
                user_id = parts[0].strip()
                username = parts[1].strip() if len(parts) > 1 else None
                
                clients.append({
                    "user_id": user_id,
                    "username": username
                })
    
    return clients


@router.delete("/{campaign_id}/processed/{user_id}")
async def remove_processed_client(campaign_id: str, user_id: str):
    """Удалить клиента из списка обработанных"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    runtime_path = Path(f"backend/campaigns_runtime/{campaign_id}")
    processed_file = runtime_path / "processed_clients.txt"
    
    if not processed_file.exists():
        raise HTTPException(status_code=404, detail="Processed file not found")
    
    # Читаем все строки
    with open(processed_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Фильтруем нужного пользователя
    new_lines = []
    found = False
    for line in lines:
        if line.strip():
            parts = line.strip().split("|", 1)
            if parts[0].strip() == user_id:
                found = True
                continue  # Пропускаем эту строку
            new_lines.append(line)
    
    if not found:
        raise HTTPException(status_code=404, detail="User not found in processed list")
    
    # Записываем обратно
    with open(processed_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    return {"message": "User removed from processed list", "user_id": user_id}

