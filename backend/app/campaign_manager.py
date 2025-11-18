"""
Campaign Manager
Управляет запуском/остановкой worker процессов для кампаний
"""
import asyncio
import json
import os
import signal
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


class CampaignManager:
    """Менеджер кампаний"""
    
    def __init__(self):
        self.campaigns: Dict[str, dict] = {}
        self.processes: Dict[str, subprocess.Popen] = {}
        self.campaigns_dir = Path("backend/campaigns")
        self.runtime_dir = Path("backend/campaigns_runtime")
        
        # Создаем папки
        self.campaigns_dir.mkdir(parents=True, exist_ok=True)
        self.runtime_dir.mkdir(parents=True, exist_ok=True)
        
        # Загружаем кампании
        self.load_campaigns()
    
    def load_campaigns(self):
        """Загружает все кампании из файлов"""
        if not self.campaigns_dir.exists():
            return
        
        for file in self.campaigns_dir.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    campaign = json.load(f)
                    self.campaigns[campaign["id"]] = campaign
                    print(f"✅ Loaded campaign: {campaign['name']} ({campaign['id']})")
            except Exception as e:
                print(f"❌ Failed to load campaign {file}: {e}")
    
    def save_campaign(self, campaign: dict):
        """Сохраняет кампанию в файл"""
        campaign_id = campaign["id"]
        file_path = self.campaigns_dir / f"{campaign_id}.json"
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(campaign, f, indent=2, ensure_ascii=False)
        
        self.campaigns[campaign_id] = campaign
        print(f"💾 Saved campaign: {campaign['name']} ({campaign_id})")
    
    def get_campaign(self, campaign_id: str) -> Optional[dict]:
        """Получает кампанию по ID"""
        return self.campaigns.get(campaign_id)
    
    def delete_campaign(self, campaign_id: str):
        """Удаляет кампанию"""
        # Останавливаем если запущена
        if campaign_id in self.processes:
            self.stop_campaign(campaign_id)
        
        # Удаляем файл
        file_path = self.campaigns_dir / f"{campaign_id}.json"
        if file_path.exists():
            file_path.unlink()
        
        # Удаляем runtime папку
        runtime_path = self.runtime_dir / campaign_id
        if runtime_path.exists():
            shutil.rmtree(runtime_path)
        
        # Удаляем из памяти
        if campaign_id in self.campaigns:
            del self.campaigns[campaign_id]
        
        print(f"🗑️ Deleted campaign: {campaign_id}")
    
    def prepare_runtime_env(self, campaign: dict) -> Path:
        """Подготавливает runtime окружение для кампании"""
        campaign_id = campaign["id"]
        runtime_path = self.runtime_dir / campaign_id
        runtime_path.mkdir(parents=True, exist_ok=True)
        
        # Создаем data папку
        data_path = runtime_path / "data"
        data_path.mkdir(exist_ok=True)
        (data_path / "sessions").mkdir(exist_ok=True)
        (data_path / "convos").mkdir(exist_ok=True)
        
        # Копируем worker скрипт
        worker_template = Path("campaigns_runtime/13e4b209-4788-43bb-a27e-40b177d41ca8/main.py")
        if worker_template.exists():
            shutil.copy(worker_template, runtime_path / "main.py")
        
        # Создаем config.json для worker
        config = self.generate_worker_config(campaign, runtime_path)
        with open(runtime_path / "config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        # Копируем сессии из общей папки если есть
        for account in campaign.get("accounts", []):
            session_name = account.get("session_name")
            if session_name:
                src_session = Path(f"backend/data/sessions/{session_name}.session")
                src_json = Path(f"backend/data/sessions/{session_name}.json")
                
                if src_session.exists():
                    shutil.copy(src_session, data_path / "sessions")
                if src_json.exists():
                    shutil.copy(src_json, data_path / "sessions")
        
        # Создаем api_map.txt
        api_map_lines = []
        for account in campaign.get("accounts", []):
            session_name = account.get("session_name")
            api_id = account.get("api_id")
            api_hash = account.get("api_hash")
            if session_name and api_id and api_hash:
                api_map_lines.append(f"{session_name}.session {api_id} {api_hash}")
        
        with open(runtime_path / "api_map.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(api_map_lines))
        
        # Создаем prompt.txt
        prompt = campaign.get("openai_settings", {}).get("system_prompt", "")
        with open(runtime_path / "prompt.txt", "w", encoding="utf-8") as f:
            f.write(prompt)
        
        # Создаем proxies.txt (опционально)
        proxy_list = campaign.get("proxy_list", "")
        if proxy_list:
            with open(runtime_path / "proxies.txt", "w", encoding="utf-8") as f:
                f.write(proxy_list)
        
        # Создаем processed_clients.txt
        processed_file = runtime_path / "processed_clients.txt"
        if not processed_file.exists():
            processed_file.touch()
        
        return runtime_path
    
    def generate_worker_config(self, campaign: dict, runtime_path: Path) -> dict:
        """Генерирует конфиг для worker из настроек кампании"""
        openai = campaign.get("openai_settings", {})
        telegram = campaign.get("telegram_settings", {})
        
        return {
            "WORK_FOLDER": str(runtime_path / "data"),
            "PROCESSED_CLIENTS": str(runtime_path / "processed_clients.txt"),
            "PROJECT_NAME": openai.get("project_name", ""),
            "OPENAI": {
                "API_KEY": openai.get("api_key", ""),
                "MODEL": openai.get("model", "gpt-4"),
                "PROXY": openai.get("proxy") if openai.get("proxy") else None,
                "SYSTEM_TXT": str(runtime_path / "prompt.txt"),
                "TRIGGER_PHRASES": {
                    "POSITIVE": openai.get("trigger_phrases_positive", "ИНТЕРЕСНО"),
                    "NEGATIVE": openai.get("trigger_phrases_negative", "НЕ_ИНТЕРЕСНО")
                },
                "TARGET_CHATS": {
                    "POSITIVE": openai.get("target_chats_positive", ""),
                    "NEGATIVE": openai.get("target_chats_negative", "")
                },
                "USE_FALLBACK_ON_OPENAI_FAIL": openai.get("use_fallback_on_fail", False),
                "FALLBACK_TEXT": openai.get("fallback_text", "")
            },
            "TELEGRAM_FORWARD_LIMIT": telegram.get("forward_limit", 5),
            "REPLY_ONLY_IF_PREVIOUSLY_WROTE": telegram.get("reply_only_if_previously_wrote", True),
            "TELEGRAM_HISTORY_LIMIT": telegram.get("history_limit", 20),
            "PRE_READ_DELAY_RANGE": telegram.get("pre_read_delay_range", [5, 10]),
            "READ_REPLY_DELAY_RANGE": telegram.get("read_reply_delay_range", [5, 10]),
            "ACCOUNT_LOOP_DELAY_RANGE": telegram.get("account_loop_delay_range", [90, 180]),
            "CHECK_NEW_MSG_INTERVAL_RANGE": telegram.get("check_new_msg_interval_range", [7, 12]),
            "DIALOG_WAIT_WINDOW_RANGE": telegram.get("dialog_wait_window_range", [40, 60]),
            "SLEEP_PERIODS": telegram.get("sleep_periods", []),
            "TIMEZONE_OFFSET": telegram.get("timezone_offset", 3)
        }
    
    async def start_campaign(self, campaign_id: str) -> bool:
        """Запускает кампанию"""
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            print(f"❌ Campaign {campaign_id} not found")
            return False
        
        # Проверяем не запущена ли уже
        if campaign_id in self.processes:
            proc = self.processes[campaign_id]
            if proc.poll() is None:  # Процесс еще работает
                print(f"⚠️ Campaign {campaign_id} already running")
                return False
        
        # Подготавливаем окружение
        print(f"🔧 Preparing runtime environment for {campaign['name']}...")
        runtime_path = self.prepare_runtime_env(campaign)
        
        # Запускаем worker процесс
        print(f"🚀 Starting worker for {campaign['name']}...")
        try:
            process = subprocess.Popen(
                ["python", "main.py"],
                cwd=str(runtime_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes[campaign_id] = process
            
            # Обновляем статус
            campaign["status"] = "running"
            self.save_campaign(campaign)
            
            print(f"✅ Campaign {campaign['name']} started (PID: {process.pid})")
            return True
        
        except Exception as e:
            print(f"❌ Failed to start campaign {campaign['name']}: {e}")
            campaign["status"] = "error"
            self.save_campaign(campaign)
            return False
    
    def stop_campaign(self, campaign_id: str) -> bool:
        """Останавливает кампанию"""
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            print(f"❌ Campaign {campaign_id} not found")
            return False
        
        if campaign_id not in self.processes:
            print(f"⚠️ Campaign {campaign_id} not running")
            campaign["status"] = "stopped"
            self.save_campaign(campaign)
            return False
        
        process = self.processes[campaign_id]
        
        try:
            # Пробуем graceful shutdown
            print(f"🛑 Stopping campaign {campaign['name']}...")
            process.terminate()
            
            # Ждем до 10 секунд
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                # Если не остановился, убиваем
                print(f"⚠️ Force killing campaign {campaign['name']}...")
                process.kill()
                process.wait()
            
            del self.processes[campaign_id]
            
            # Обновляем статус
            campaign["status"] = "stopped"
            self.save_campaign(campaign)
            
            print(f"✅ Campaign {campaign['name']} stopped")
            return True
        
        except Exception as e:
            print(f"❌ Failed to stop campaign {campaign['name']}: {e}")
            return False
    
    def get_campaign_status(self, campaign_id: str) -> dict:
        """Получает статус кампании"""
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            return {"status": "not_found"}
        
        is_running = False
        pid = None
        
        if campaign_id in self.processes:
            proc = self.processes[campaign_id]
            if proc.poll() is None:
                is_running = True
                pid = proc.pid
            else:
                # Процесс завершился
                del self.processes[campaign_id]
        
        # Обновляем статус если нужно
        if is_running and campaign["status"] != "running":
            campaign["status"] = "running"
            self.save_campaign(campaign)
        elif not is_running and campaign["status"] == "running":
            campaign["status"] = "stopped"
            self.save_campaign(campaign)
        
        return {
            "status": campaign["status"],
            "is_running": is_running,
            "pid": pid
        }
    
    async def restore_running_campaigns(self):
        """Восстанавливает запущенные кампании после перезапуска"""
        print("🔄 Checking for campaigns to restore...")
        for campaign_id, campaign in self.campaigns.items():
            if campaign.get("status") == "running":
                print(f"🔄 Restoring campaign: {campaign['name']}")
                await self.start_campaign(campaign_id)
    
    async def stop_all_campaigns(self):
        """Останавливает все запущенные кампании"""
        print("🛑 Stopping all campaigns...")
        for campaign_id in list(self.processes.keys()):
            self.stop_campaign(campaign_id)


# Глобальный экземпляр менеджера
campaign_manager = CampaignManager()

