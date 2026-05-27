"""
账号管理应用配置
负责用户认证、注册、权限管理等功能
"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = '账号管理'
