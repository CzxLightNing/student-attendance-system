"""
管理面板应用的视图定义
Admin panel app view definitions
包含班级管理、用户管理、CSV 批量导入、考勤总览等功能
Includes class management, user management, CSV batch import, attendance overview
管理员使用函数视图 + 部分 CBV 实现
Admin uses function views with some CBV implementation
"""
import csv
import os
import logging
from io import StringIO, BytesIO
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, FileResponse
from django.conf import settings
from django.db.models import Count, Q
from django.core.exceptions import ValidationError
from accounts.decorators import AdminRequiredMixin
from attendance.models import Class, AttendanceCode, AttendanceRecord

User = get_user_model()
audit_logger = logging.getLogger('audit')

# ==================== CSV 上传安全校验常量 ====================
# ==================== CSV Upload Security Validation Constants ====================
ALLOWED_EXTENSIONS = ['.csv']
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB


def validate_csv_upload(file):
    """
    CSV 文件上传安全校验函数
    CSV file upload security validation function
    执行三重校验：文件扩展名 + MIME 类型 + 文件大小
    Three checks: file extension + MIME type + file size
    """
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError('仅允许上传 .csv 格式文件')
    if file.size > MAX_UPLOAD_SIZE:
        raise ValidationError(f'文件大小不能超过 {MAX_UPLOAD_SIZE // (1024 * 1024)}MB')
    if file.content_type != 'text/csv':
        raise ValidationError('文件类型不正确，仅支持 CSV 文件')


# ==================== 管理面板首页 ====================
# ==================== Admin Panel Home ====================

class ManagementHomeView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    """管理员主页：考勤总览统计"""
    """Admin home: attendance overview statistics"""
    template_name = 'management/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_classes'] = Class.objects.count()
        context['total_teachers'] = User.objects.filter(role='teacher').count()
        context['total_students'] = User.objects.filter(role='student').count()
        context['total_records'] = AttendanceRecord.objects.count()
        context['pending_users'] = User.objects.filter(is_active=False).count()
        today = datetime.now().date()
        context['today_records'] = AttendanceRecord.objects.filter(
            timestamp__date=today
        ).count()
        return context


# ==================== 班级管理视图 ====================
# ==================== Class Management Views ====================

class ClassListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """班级列表视图"""
    """Class list view"""
    template_name = 'management/class_list.html'
    model = Class
    context_object_name = 'classes'
    paginate_by = 20


class ClassCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """创建班级视图"""
    template_name = 'management/class_form.html'
    model = Class
    fields = ['name', 'grade']
    success_url = reverse_lazy('management_app:management_class_list')

    def form_valid(self, form):
        audit_logger.info(f'创建班级 - 班级:{form.instance.name} 管理员:{self.request.user.username}')
        messages.success(self.request, f'班级 "{form.instance.name}" 创建成功!')
        return super().form_valid(form)


class ClassUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """编辑班级视图"""
    """Edit class view"""
    template_name = 'management/class_form.html'
    model = Class
    fields = ['name', 'grade']
    success_url = reverse_lazy('management_app:management_class_list')
    pk_url_kwarg = 'class_id'

    def form_valid(self, form):
        audit_logger.info(f'编辑班级 - 班级:{form.instance.name} 管理员:{self.request.user.username}')
        messages.success(self.request, f'班级 "{form.instance.name}" 更新成功!')
        return super().form_valid(form)


class ClassDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """删除班级视图"""
    model = Class
    pk_url_kwarg = 'class_id'
    success_url = reverse_lazy('management_app:management_class_list')

    def post(self, request, *args, **kwargs):
        class_group = self.get_object()
        audit_logger.info(f'删除班级 - 班级:{class_group.name} 管理员:{request.user.username}')
        messages.success(request, f'班级 "{class_group.name}" 已删除!')
        return super().post(request, *args, **kwargs)


class ClassCSVImportView(LoginRequiredMixin, AdminRequiredMixin, View):
    """CSV 批量导入班级视图"""
    template_name = 'management/csv_import.html'

    def get(self, request):
        return render(request, self.template_name, {
            'import_type': '班级',
            'action_url': reverse('management_app:management_class_csv_import'),
            'template_url': reverse('management_app:management_csv_template', kwargs={'template_name': 'classes_template.csv'}),
        })

    def post(self, request):
        file = request.FILES.get('csv_file')
        if not file:
            messages.error(request, '请选择要上传的 CSV 文件')
            return render(request, self.template_name, {
                'import_type': '班级',
                'action_url': reverse('management_app:management_class_csv_import'),
                'template_url': reverse('management_app:management_csv_template', kwargs={'template_name': 'classes_template.csv'}),
            })

        try:
            validate_csv_upload(file)
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, self.template_name, {
                'import_type': '班级',
                'action_url': reverse('management_app:management_class_csv_import'),
                'template_url': reverse('management_app:management_csv_template', kwargs={'template_name': 'classes_template.csv'}),
            })

        try:
            file_content = file.read().decode('utf-8-sig')
            reader = csv.DictReader(StringIO(file_content))
            success_count = 0
            error_rows = []

            for row_num, row in enumerate(reader, start=2):
                name = row.get('班级名称', '').strip()
                grade = row.get('年级', '').strip()
                if not name or not grade:
                    error_rows.append(f'第 {row_num} 行：班级名称和年级不能为空')
                    continue
                if Class.objects.filter(name=name).exists():
                    error_rows.append(f'第 {row_num} 行：班级 "{name}" 已存在')
                    continue
                Class.objects.create(name=name, grade=grade)
                success_count += 1

            if error_rows:
                messages.warning(request, f'导入完成：成功 {success_count} 条。以下行有错误：{";".join(error_rows[:5])}')
            else:
                messages.success(request, f'成功导入 {success_count} 个班级!')

            audit_logger.info(f'CSV导入班级 - 成功:{success_count} 管理员:{request.user.username}')

        except Exception as e:
            messages.error(request, f'CSV 文件解析失败：{str(e)}')

        return redirect('management_app:management_class_list')


# ==================== 用户管理视图 ====================
# ==================== User Management Views ====================

class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """用户列表视图，支持按角色和班级筛选"""
    """User list view, supports filtering by role and class"""
    template_name = 'management/user_list.html'
    model = User
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        queryset = User.objects.all().order_by('role', '-date_joined')
        role = self.request.GET.get('role', '')
        class_id = self.request.GET.get('class_id', '')

        if role:
            queryset = queryset.filter(role=role)
        if class_id:
            queryset = queryset.filter(student_class_id=class_id)

        return queryset.select_related('student_class')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role_filter'] = self.request.GET.get('role', '')
        context['class_filter'] = self.request.GET.get('class_id', '')
        context['all_classes'] = Class.objects.all()
        return context


class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, View):
    """管理员手动创建用户（学生或教师）"""
    """Admin manually creates user (student or teacher)"""
    template_name = 'management/user_form.html'

    def get(self, request):
        return render(request, self.template_name, {
            'action': '创建',
            'edit_user': None,
            'form_data': {},
            'errors': None,
            'classes': Class.objects.all(),
        })

    def post(self, request):
        username = request.POST.get('username', '').strip()
        role = request.POST.get('role', 'student')
        last_name = request.POST.get('last_name', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        email = request.POST.get('email', '').strip()
        student_id = request.POST.get('student_id', '').strip()
        teacher_id = request.POST.get('teacher_id', '').strip()
        class_id = request.POST.get('class_id', '').strip()

        errors = []
        if not username:
            errors.append('请输入用户名')
        if User.objects.filter(username=username).exists():
            errors.append('该用户名已存在')
        if role == 'student' and not student_id:
            errors.append('学生必须填写学号')
        if role == 'teacher' and not teacher_id:
            errors.append('教师必须填写工号')

        if errors:
            return render(request, self.template_name, {
                'action': '创建',
                'edit_user': None,
                'classes': Class.objects.all(),
                'errors': errors,
                'form_data': request.POST.dict(),
            })

        student_class = None
        if class_id:
            student_class = get_object_or_404(Class, id=class_id)

        user = User.objects.create_user(
            username=username,
            password='12345678',
            email=email,
            last_name=last_name,
            first_name=first_name,
            role=role,
            student_id=student_id if role == 'student' else None,
            teacher_id=teacher_id if role == 'teacher' else None,
            student_class=student_class if role == 'student' else None,
            is_active=True,
        )

        audit_logger.info(f'管理员创建用户 - 用户名:{username} 角色:{role} 操作者:{request.user.username}')
        messages.success(request, f'用户 "{username}" 创建成功! 初始密码为 12345678')
        return redirect('management_app:management_user_list')


class UserEditView(LoginRequiredMixin, AdminRequiredMixin, View):
    """管理员编辑用户信息"""
    """Admin edits user info"""
    template_name = 'management/user_form.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, self.template_name, {
            'action': '编辑',
            'edit_user': user,
            'form_data': {},
            'classes': Class.objects.all(),
        })

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.last_name = request.POST.get('last_name', '').strip()
        user.first_name = request.POST.get('first_name', '').strip()
        user.email = request.POST.get('email', '').strip()

        if user.role == 'student':
            user.student_id = request.POST.get('student_id', '').strip() or None
            class_id = request.POST.get('class_id', '').strip()
            user.student_class = get_object_or_404(Class, id=class_id) if class_id else None

        if user.role == 'teacher':
            user.teacher_id = request.POST.get('teacher_id', '').strip() or None

        user.save()
        audit_logger.info(f'管理员编辑用户 - 用户名:{user.username} 操作者:{request.user.username}')
        messages.success(request, f'用户 "{user.username}" 信息已更新!')
        return redirect('management_app:management_user_list')


class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, View):
    """管理员删除用户"""
    """Admin deletes user"""
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user.id == request.user.id:
            messages.error(request, '不能删除自己的账号!')
            return redirect('management_app:management_user_list')

        username = user.username
        user.delete()
        audit_logger.warning(f'管理员删除用户 - 用户名:{username} 操作者:{request.user.username}')
        messages.success(request, f'用户 "{username}" 已删除!')
        return redirect('management_app:management_user_list')


class UserResetPasswordView(LoginRequiredMixin, AdminRequiredMixin, View):
    """管理员重置用户密码为初始密码 12345678"""
    """Admin resets user password to default 12345678"""
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.set_password('12345678')
        user.save()

        ip = request.META.get('REMOTE_ADDR', 'unknown')
        audit_logger.warning(f'管理员重置密码 - 目标用户:{user.username} 操作者:{request.user.username} IP:{ip}')
        messages.success(request, f'用户 "{user.username}" 的密码已重置为 12345678')
        return redirect('management_app:management_user_list')


class UserActivateView(LoginRequiredMixin, AdminRequiredMixin, View):
    """管理员审核/激活用户自行注册的账号"""
    """Admin reviews/activates self-registered accounts"""
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.is_active = True
        user.save()

        ip = request.META.get('REMOTE_ADDR', 'unknown')
        audit_logger.info(f'管理员激活账号 - 目标用户:{user.username} 操作者:{request.user.username} IP:{ip}')
        messages.success(request, f'用户 "{user.username}" 的账号已激活!')
        return redirect('management_app:management_user_list')


class UserCSVImportView(LoginRequiredMixin, AdminRequiredMixin, View):
    """CSV 批量导入用户（学生或教师）"""
    template_name = 'management/csv_import.html'

    def get(self, request):
        import_type = request.GET.get('type', 'student')
        template_map = {
            'student': 'students_template.csv',
            'teacher': 'teachers_template.csv',
        }
        return render(request, self.template_name, {
            'import_type': '学生' if import_type == 'student' else '教师',
            'import_role': import_type,
            'action_url': reverse('management_app:management_user_csv_import') + f'?type={import_type}',
            'template_url': reverse('management_app:management_csv_template', kwargs={'template_name': template_map.get(import_type, '')}),
        })

    def post(self, request):
        import_type = request.GET.get('type', 'student')
        file = request.FILES.get('csv_file')
        if not file:
            messages.error(request, '请选择要上传的 CSV 文件')
            return redirect('management_app:management_user_list')

        try:
            validate_csv_upload(file)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('management_app:management_user_list')

        try:
            file_content = file.read().decode('utf-8-sig')
            reader = csv.DictReader(StringIO(file_content))
            success_count = 0
            error_rows = []

            for row_num, row in enumerate(reader, start=2):
                if import_type == 'student':
                    username = row.get('用户名', '').strip()
                    student_id = row.get('学号', '').strip()
                    name = row.get('姓名', '').strip()
                    class_name = row.get('所属班级名称', '').strip()

                    if not username or not student_id or not name or not class_name:
                        error_rows.append(f'第 {row_num} 行：必填字段不能为空')
                        continue
                    if User.objects.filter(username=username).exists():
                        error_rows.append(f'第 {row_num} 行：用户名 "{username}" 已存在')
                        continue
                    if User.objects.filter(student_id=student_id).exists():
                        error_rows.append(f'第 {row_num} 行：学号 "{student_id}" 已存在')
                        continue

                    student_class = Class.objects.filter(name=class_name).first()
                    if not student_class:
                        error_rows.append(f'第 {row_num} 行：班级 "{class_name}" 不存在')
                        continue

                    User.objects.create_user(
                        username=username,
                        password='12345678',
                        last_name=name,
                        first_name='',
                        role='student',
                        student_id=student_id,
                        student_class=student_class,
                        is_active=True,
                    )
                    success_count += 1

                else:
                    username = row.get('用户名', '').strip()
                    teacher_id = row.get('工号', '').strip()
                    name = row.get('姓名', '').strip()
                    email = row.get('邮箱', '').strip()
                    class_names_str = row.get('管理的班级名称', '').strip()

                    if not username or not teacher_id or not name:
                        error_rows.append(f'第 {row_num} 行：必填字段不能为空')
                        continue
                    if User.objects.filter(username=username).exists():
                        error_rows.append(f'第 {row_num} 行：用户名 "{username}" 已存在')
                        continue
                    if teacher_id and User.objects.filter(teacher_id=teacher_id).exists():
                        error_rows.append(f'第 {row_num} 行：工号 "{teacher_id}" 已存在')
                        continue

                    teacher = User.objects.create_user(
                        username=username,
                        password='12345678',
                        last_name=name,
                        first_name='',
                        email=email,
                        role='teacher',
                        teacher_id=teacher_id,
                        is_active=True,
                    )

                    if class_names_str:
                        class_names = [cn.strip() for cn in class_names_str.split('；') if cn.strip()]
                        managed_classes = Class.objects.filter(name__in=class_names)
                        teacher.managed_classes.set(managed_classes)

                    success_count += 1

            if error_rows:
                messages.warning(request, f'导入完成：成功 {success_count} 条。以下行有错误：{";".join(error_rows[:5])}')
            else:
                messages.success(request, f'成功导入 {success_count} 条记录!')

            audit_logger.info(f'CSV导入用户 - 类型:{import_type} 成功:{success_count} 管理员:{request.user.username}')

        except Exception as e:
            messages.error(request, f'CSV 文件解析失败：{str(e)}')

        return redirect('management_app:management_user_list')


# ==================== CSV 模板下载 ====================
# ==================== CSV Template Download ====================

class CSVTemplateDownloadView(LoginRequiredMixin, AdminRequiredMixin, View):
    """CSV 模板文件下载视图"""
    def get(self, request, template_name):
        template_path = os.path.join(
            settings.BASE_DIR, 'static', 'csv_templates', template_name
        )
        if os.path.exists(template_path):
            return FileResponse(
                open(template_path, 'rb'),
                as_attachment=True,
                filename=template_name,
                content_type='text/csv',
            )
        messages.error(request, f'模板文件 "{template_name}" 不存在')
        return redirect('management_app:management_home')


# ==================== 考勤总览视图（管理员） ====================
# ==================== Attendance Overview View (Admin) ====================

class AdminAttendanceOverviewView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    """管理员考勤总览：查看所有班级的签到统计"""
    """Admin attendance overview: view stats for all classes"""
    template_name = 'management/attendance_overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classes = Class.objects.all().prefetch_related('attendancecode_set').order_by('grade', 'name')
        class_stats = []

        for class_group in classes:
            total_students = User.objects.filter(
                role='student', student_class=class_group
            ).count()

            latest_code = AttendanceCode.objects.filter(
                class_group=class_group
            ).order_by('-created_at').first()

            latest_info = None
            if latest_code:
                signed_count = AttendanceRecord.objects.filter(
                    attendance_code=latest_code
                ).count()
                latest_info = {
                    'code': latest_code.code,
                    'created_at': latest_code.created_at,
                    'signed_count': signed_count,
                    'total': total_students,
                }

            class_stats.append({
                'id': class_group.id,
                'name': class_group.name,
                'grade': class_group.grade,
                'total_students': total_students,
                'latest_attendance': latest_info,
            })

        context['class_stats'] = class_stats
        return context
