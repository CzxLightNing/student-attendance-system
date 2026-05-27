"""
管理面板应用的 URL 路由配置
Admin panel app URL routing configuration
包含班级管理、用户管理、CSV 导入导出、考勤总览等路由
"""
from django.urls import path
from . import views

app_name = 'management_app'

urlpatterns = [
    # 管理面板首页
    # Admin panel home
    path('', views.ManagementHomeView.as_view(), name='management_home'),

    # ==================== 班级管理路由 ====================
    # ==================== Class Management Routes ====================
    # 班级列表
    # Class list
    path('classes/', views.ClassListView.as_view(), name='management_class_list'),
    # 创建班级
    # Create class
    path('classes/create/', views.ClassCreateView.as_view(), name='management_class_create'),
    # 编辑班级
    # Edit class
    path('classes/<int:class_id>/edit/', views.ClassUpdateView.as_view(), name='management_class_edit'),
    # 删除班级
    # Delete class
    path('classes/<int:class_id>/delete/', views.ClassDeleteView.as_view(), name='management_class_delete'),
    # CSV 批量导入班级
    # CSV batch import classes
    path('classes/csv-import/', views.ClassCSVImportView.as_view(), name='management_class_csv_import'),

    # ==================== 用户管理路由 ====================
    # ==================== User Management Routes ====================
    # 用户列表
    # User list
    path('users/', views.UserListView.as_view(), name='management_user_list'),
    # 创建用户
    # Create user
    path('users/create/', views.UserCreateView.as_view(), name='management_user_create'),
    # 编辑用户
    # Edit user
    path('users/<int:user_id>/edit/', views.UserEditView.as_view(), name='management_user_edit'),
    # 删除用户
    # Delete user
    path('users/<int:user_id>/delete/', views.UserDeleteView.as_view(), name='management_user_delete'),
    # 重置用户密码
    # Reset user password
    path('users/<int:user_id>/reset-password/', views.UserResetPasswordView.as_view(), name='management_user_reset_password'),
    # 激活用户账号
    # Activate user account
    path('users/<int:user_id>/activate/', views.UserActivateView.as_view(), name='management_user_activate'),
    # CSV 批量导入用户
    # CSV batch import users
    path('users/csv-import/', views.UserCSVImportView.as_view(), name='management_user_csv_import'),

    # ==================== CSV 模板下载 ====================
    # ==================== CSV Template Download ====================
    path('csv-template/<str:template_name>/', views.CSVTemplateDownloadView.as_view(), name='management_csv_template'),

    # ==================== 考勤总览 ====================
    # ==================== Attendance Overview ====================
    path('attendance-overview/', views.AdminAttendanceOverviewView.as_view(), name='management_attendance_overview'),
]
