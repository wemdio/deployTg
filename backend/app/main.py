"""
TG Auto-Responder Backend
FastAPI приложение для управления Telegram кампаниями
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .api import campaigns, accounts, dialogs
from .campaign_manager import campaign_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager для FastAPI"""
    # Startup
    print("=" * 80)
    print("🚀 TG Auto-Responder Backend Starting...")
    print("=" * 80)
    
    # Создаем необходимые папки
    os.makedirs("backend/campaigns", exist_ok=True)
    os.makedirs("backend/campaigns_runtime", exist_ok=True)
    os.makedirs("backend/data/sessions", exist_ok=True)
    
    # Восстанавливаем запущенные кампании после перезапуска
    await campaign_manager.restore_running_campaigns()
    
    yield
    
    # Shutdown
    print("=" * 80)
    print("🛑 TG Auto-Responder Backend Shutting down...")
    print("=" * 80)
    
    # Останавливаем все кампании
    await campaign_manager.stop_all_campaigns()


# Создаем FastAPI приложение
app = FastAPI(
    title="TG Auto-Responder API",
    description="API для управления Telegram авто-ответчиком",
    version="1.0.0",
    lifespan=lifespan
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.twc1.net",
        "*"  # В production лучше указать конкретные домены
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(campaigns.router, prefix="/campaigns", tags=["Campaigns"])
app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
app.include_router(dialogs.router, prefix="/dialogs", tags=["Dialogs"])


@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "name": "TG Auto-Responder API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check для Timeweb"""
    running_campaigns = len([
        c for c in campaign_manager.campaigns.values()
        if c.get("status") == "running"
    ])
    
    return {
        "status": "healthy",
        "running_campaigns": running_campaigns,
        "total_campaigns": len(campaign_manager.campaigns)
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Глобальный обработчик ошибок"""
    print(f"❌ Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

