"""
管理面板应用配置
负责管理员后台的班级管理、用户管理、考勤总览等功能
"""
from django.apps import AppConfig


class ManagementAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'management_app'
    verbose_name = '管理面板'
