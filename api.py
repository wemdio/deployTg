"""
Точка входа для FastAPI backend на Timeweb Cloud
Worker (main.py) запускается как subprocess через campaign_manager
"""
from app.main import app

__all__ = ['app']

