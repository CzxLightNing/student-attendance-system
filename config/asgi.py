"""
Django ASGI 应用入口
用于在生产环境中通过 ASGI 服务器（如 Daphne、Uvicorn）部署 Django 应用
支持异步通信协议（WebSocket 等）
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
