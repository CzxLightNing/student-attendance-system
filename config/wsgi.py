"""
Django WSGI 应用入口
Django WSGI application entry point
用于在生产环境中通过 WSGI 服务器（如 Gunicorn、uWSGI）部署 Django 应用
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
