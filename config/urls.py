"""
Django 主 URL 路由配置
Django main URL routing config
将根路径及各个应用的 URL 分发到对应的子路由模块
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Django 内置管理后台
    # Django built-in admin backend
    path('admin/', admin.site.urls),
    # 账号认证相关路由（登录、注册、登出、修改密码）
    # Account auth routes (login, register, logout, change password)
    path('accounts/', include('accounts.urls')),
    # 签到考勤相关路由（学生签到、教师管理签到码）
    # Attendance routes (student check-in, teacher code management)
    path('attendance/', include('attendance.urls')),
    # 管理面板路由
    # Admin panel routes
    path('management/', include('management_app.urls')),
    # 首页：根据角色重定向
    # Home page: redirect by role
    path('', RedirectView.as_view(pattern_name='accounts:home', permanent=False), name='root'),
]
