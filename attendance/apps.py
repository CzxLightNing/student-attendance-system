"""
签到考勤应用配置
负责签到码生成、学生签到、考勤记录管理等功能
"""
from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendance'
    verbose_name = '签到考勤'
