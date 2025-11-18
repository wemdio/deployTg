"""
Campaigns API Router
Управление кампаниями
"""
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..campaign_manager import campaign_manager


router = APIRouter()


# Pydantic модели
class OpenAISettings(BaseModel):
    api_key: str = ""
    model: str = "gpt-4"
    proxy: Optional[str] = None
    system_prompt: str = ""
    project_name: str = ""
    trigger_phrases_positive: str = "ИНТЕРЕСНО"
    trigger_phrases_negative: str = "НЕ_ИНТЕРЕСНО"
    target_chats_positive: str = ""
    target_chats_negative: str = ""
    use_fallback_on_fail: bool = False
    fallback_text: str = ""


class TelegramSettings(BaseModel):
    forward_limit: int = 5
    reply_only_if_previously_wrote: bool = True
    history_limit: int = 20
    pre_read_delay_range: List[float] = [5.0, 10.0]
    read_reply_delay_range: List[float] = [5.0, 10.0]
    account_loop_delay_range: List[float] = [90.0, 180.0]
    check_new_msg_interval_range: List[float] = [7.0, 12.0]
    dialog_wait_window_range: List[float] = [40.0, 60.0]
    sleep_periods: List[str] = []
    timezone_offset: int = 3


class CampaignCreate(BaseModel):
    name: str
    openai_settings: Optional[OpenAISettings] = None
    telegram_settings: Optional[TelegramSettings] = None


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    openai_settings: Optional[OpenAISettings] = None
    telegram_settings: Optional[TelegramSettings] = None


@router.get("/")
async def get_campaigns():
    """Получить список всех кампаний"""
    campaigns = list(campaign_manager.campaigns.values())
    
    # Обновляем статусы
    for campaign in campaigns:
        status = campaign_manager.get_campaign_status(campaign["id"])
        campaign["is_running"] = status["is_running"]
    
    return campaigns


@router.post("/")
async def create_campaign(campaign_data: CampaignCreate):
    """Создать новую кампанию"""
    campaign_id = str(uuid.uuid4())
    
    campaign = {
        "id": campaign_id,
        "name": campaign_data.name,
        "status": "stopped",
        "accounts": [],
        "openai_settings": campaign_data.openai_settings.dict() if campaign_data.openai_settings else OpenAISettings().dict(),
        "telegram_settings": campaign_data.telegram_settings.dict() if campaign_data.telegram_settings else TelegramSettings().dict(),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    campaign_manager.save_campaign(campaign)
    
    return campaign


@router.get("/{campaign_id}")
async def get_campaign(campaign_id: str):
    """Получить кампанию по ID"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Обновляем статус
    status = campaign_manager.get_campaign_status(campaign_id)
    campaign["is_running"] = status["is_running"]
    campaign["pid"] = status.get("pid")
    
    return campaign


@router.put("/{campaign_id}")
async def update_campaign(campaign_id: str, updates: CampaignUpdate):
    """Обновить кампанию"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Обновляем поля
    if updates.name is not None:
        campaign["name"] = updates.name
    
    if updates.openai_settings is not None:
        campaign["openai_settings"] = updates.openai_settings.dict()
    
    if updates.telegram_settings is not None:
        campaign["telegram_settings"] = updates.telegram_settings.dict()
    
    campaign["updated_at"] = datetime.now().isoformat()
    
    campaign_manager.save_campaign(campaign)
    
    return campaign


@router.delete("/{campaign_id}")
async def delete_campaign(campaign_id: str):
    """Удалить кампанию"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    campaign_manager.delete_campaign(campaign_id)
    
    return {"message": "Campaign deleted", "id": campaign_id}


@router.post("/{campaign_id}/start")
async def start_campaign(campaign_id: str):
    """Запустить кампанию"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Проверяем есть ли аккаунты
    if not campaign.get("accounts"):
        raise HTTPException(status_code=400, detail="Cannot start campaign without accounts")
    
    # Проверяем OpenAI ключ
    if not campaign.get("openai_settings", {}).get("api_key"):
        raise HTTPException(status_code=400, detail="OpenAI API key is required")
    
    success = await campaign_manager.start_campaign(campaign_id)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to start campaign")
    
    return {"message": "Campaign started", "id": campaign_id}


@router.post("/{campaign_id}/stop")
async def stop_campaign(campaign_id: str):
    """Остановить кампанию"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    success = campaign_manager.stop_campaign(campaign_id)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to stop campaign")
    
    return {"message": "Campaign stopped", "id": campaign_id}


@router.get("/{campaign_id}/status")
async def get_campaign_status(campaign_id: str):
    """Получить статус кампании"""
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    status = campaign_manager.get_campaign_status(campaign_id)
    
    return {
        "id": campaign_id,
        "name": campaign["name"],
        **status
    }


@router.get("/{campaign_id}/logs")
async def get_campaign_logs(campaign_id: str, limit: int = 100):
    """Получить логи кампании"""
    import os
    from pathlib import Path
    
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    runtime_path = Path(f"backend/campaigns_runtime/{campaign_id}")
    error_log = runtime_path / "errors.log"
    
    logs = []
    
    if error_log.exists():
        with open(error_log, "r", encoding="utf-8") as f:
            lines = f.readlines()
            logs = [line.strip() for line in lines[-limit:]]
    
    return {
        "campaign_id": campaign_id,
        "logs": logs,
        "total": len(logs)
    }


@router.get("/{campaign_id}/stats")
async def get_campaign_stats(campaign_id: str):
    """Получить статистику кампании"""
    from pathlib import Path
    
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    runtime_path = Path(f"backend/campaigns_runtime/{campaign_id}")
    processed_file = runtime_path / "processed_clients.txt"
    convos_dir = runtime_path / "data" / "convos"
    
    processed_count = 0
    if processed_file.exists():
        with open(processed_file, "r", encoding="utf-8") as f:
            processed_count = len([line for line in f if line.strip()])
    
    dialogs_count = 0
    if convos_dir.exists():
        dialogs_count = len(list(convos_dir.glob("*.jsonl")))
    
    return {
        "campaign_id": campaign_id,
        "campaign_name": campaign["name"],
        "status": campaign["status"],
        "accounts_count": len(campaign.get("accounts", [])),
        "processed_clients": processed_count,
        "active_dialogs": dialogs_count
    }

