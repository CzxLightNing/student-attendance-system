"""
签到考勤应用的 URL 路由配置
包含学生签到、教师签到码管理、考勤详情、导出等路由
"""
from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # ==================== 学生相关路由 ====================
    # 学生主页（签到码输入页）
    path('student/', views.StudentHomeView.as_view(), name='student_home'),
    # 学生签到 AJAX 接口
    path('student/checkin/', views.StudentCheckinView.as_view(), name='student_checkin'),
    # 学生签到历史页
    path('student/history/', views.StudentHistoryView.as_view(), name='student_history'),

    # ==================== 教师相关路由 ====================
    # 教师主页（管理的班级列表）
    path('teacher/', views.TeacherHomeView.as_view(), name='teacher_home'),
    # 班级签到管理页
    path('teacher/class/<int:class_id>/', views.TeacherClassDetailView.as_view(), name='teacher_class_detail'),
    # 生成签到码 AJAX 接口
    path('teacher/class/<int:class_id>/generate/', views.TeacherGenerateCodeView.as_view(), name='teacher_generate_code'),
    # 失效签到码 AJAX 接口
    path('teacher/class/<int:class_id>/deactivate/', views.TeacherDeactivateCodeView.as_view(), name='teacher_deactivate_code'),
    # 签到实时状态查询 AJAX 接口
    path('teacher/code/<int:code_id>/status/', views.TeacherCheckinStatusView.as_view(), name='teacher_code_status'),
    # 签到码考勤详情页
    path('teacher/code/<int:code_id>/detail/', views.TeacherAttendanceDetailView.as_view(), name='teacher_code_detail'),
    # 导出考勤 Excel
    path('teacher/code/<int:code_id>/export/', views.TeacherExportExcelView.as_view(), name='teacher_export_excel'),
    # 班级考勤历史记录
    path('teacher/class/<int:class_id>/history/', views.TeacherAttendanceHistoryView.as_view(), name='teacher_attendance_history'),
    # 班级学生名单
    path('teacher/class/<int:class_id>/students/', views.TeacherStudentListView.as_view(), name='teacher_student_list'),
]
