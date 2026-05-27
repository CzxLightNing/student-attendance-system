"""
账号管理应用的 URL 路由配置
包含登录、注册、登出、修改密码等认证相关路由
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # 首页：根据角色重定向
    path('', views.HomeView.as_view(), name='home'),
    # 用户登录
    path('login/', views.LoginView.as_view(), name='login'),
    # 用户登出
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # 用户注册
    path('register/', views.RegisterView.as_view(), name='register'),
    # 修改密码（学生和教师使用）
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]
