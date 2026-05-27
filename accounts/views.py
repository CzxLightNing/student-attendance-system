"""
账号管理应用的视图定义
Account management app view definitions
包含用户登录、注册、登出、修改密码等认证相关视图
Includes login, register, logout, change password auth views
所有视图优先使用 Django Class-Based Views 实现
All views use Django Class-Based Views by preference
"""
import logging
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView, View
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from .models import CustomUser
from .decorators import admin_required

# 创建审计日志记录器
# Create audit logger
audit_logger = logging.getLogger('audit')


class LoginView(DjangoLoginView):
    """
    用户登录视图
    User login view
    使用 Django 内置的 LoginView，自定义模板和成功跳转逻辑
    Use Django built-in LoginView with custom template and redirect logic
    登录成功后根据用户角色跳转到对应的首页
    Redirect to role-specific home page after successful login
    """
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        """
        登录表单验证通过后的处理
        Handle successful login form validation
        记录审计日志：登录成功事件
        Log audit: login success event
        """
        user = form.get_user()
        ip = self.request.META.get('REMOTE_ADDR', 'unknown')
        audit_logger.info(f'登录成功 - 用户名:{user.username} 角色:{user.role} IP:{ip}')
        messages.success(self.request, f'欢迎回来，{user.last_name}{user.first_name}！')
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        登录表单验证失败后的处理
        Handle failed login form validation
        记录审计日志：登录失败事件
        Log audit: login failure event
        """
        username = self.request.POST.get('username', 'unknown')
        ip = self.request.META.get('REMOTE_ADDR', 'unknown')
        audit_logger.warning(f'登录失败 - 尝试用户名:{username} IP:{ip}')
        messages.error(self.request, '用户名或密码错误，请重试')
        return super().form_invalid(form)

    def get_success_url(self):
        """
        登录成功后根据用户角色跳转到对应页面
        管理员 → 管理面板首页
        教师 → 教师班级列表首页
        学生 → 学生签到首页
        """
        user = self.request.user
        if user.role == 'admin':
            return reverse_lazy('management_app:management_home')
        elif user.role == 'teacher':
            return reverse_lazy('attendance:teacher_home')
        else:
            return reverse_lazy('attendance:student_home')


class LogoutView(DjangoLogoutView):
    """
    用户登出视图
    使用 Django 内置的 LogoutView，支持 GET 和 POST 请求
    登出后调用 flush() 彻底清除服务端会话数据
    """
    next_page = reverse_lazy('accounts:login')
    http_method_names = ['get', 'post', 'options']

    def dispatch(self, request, *args, **kwargs):
        """
        在登出前记录审计日志
        """
        if request.user.is_authenticated:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
            audit_logger.info(f'用户登出 - 用户名:{request.user.username} IP:{ip}')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    """
    用户注册视图
    访客可自行注册学生或教师账号
    注册后账号默认为未激活状态（is_active=False），需管理员审核后激活
    """
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        """
        处理注册表单提交
        手动创建用户并设置 argon2 哈希密码
        """
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        email = request.POST.get('email', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        role = request.POST.get('role', 'student')
        student_id = request.POST.get('student_id', '').strip()
        teacher_id = request.POST.get('teacher_id', '').strip()

        # 表单验证：必填字段检查
        # Form validation: required field check
        errors = []
        if not username:
            errors.append('请输入用户名')
        if len(password) < 6:
            errors.append('密码长度不能少于 6 位')
        if password != password_confirm:
            errors.append('两次输入的密码不一致')
        if not last_name or not first_name:
            errors.append('请输入姓名')
        if role not in ['student', 'teacher']:
            errors.append('请选择有效的角色')

        # 检查用户名是否已存在
        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            errors.append('该用户名已被使用')

        # 学生角色：学号为必填
        # Student role: student ID is required
        if role == 'student' and not student_id:
            errors.append('学生账号必须填写学号')
        if role == 'student' and student_id and CustomUser.objects.filter(student_id=student_id).exists():
            errors.append('该学号已被使用')

        # 教师角色：工号为必填
        # Teacher role: teacher ID is required
        if role == 'teacher' and not teacher_id:
            errors.append('教师账号必须填写工号')
        if role == 'teacher' and teacher_id and CustomUser.objects.filter(teacher_id=teacher_id).exists():
            errors.append('该工号已被使用')

        if errors:
            # 返回错误信息到注册页面
            # Return error messages to registration page
            return render(request, self.template_name, {
                'errors': errors,
                'form_data': request.POST,
            })

        # 创建用户，is_active 设为 False，需管理员审核激活
        # Create user; is_active set to False, requires admin approval
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            last_name=last_name,
            first_name=first_name,
            role=role,
            student_id=student_id if role == 'student' else None,
            teacher_id=teacher_id if role == 'teacher' else None,
            is_active=False,
        )

        ip = request.META.get('REMOTE_ADDR', 'unknown')
        audit_logger.info(f'用户注册 - 用户名:{username} 角色:{role} IP:{ip}')
        messages.success(request, '注册成功！请等待管理员审核激活您的账号。')
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        """显示注册页面"""
        """Display registration page"""
        return render(request, self.template_name)


class ChangePasswordView(LoginRequiredMixin, FormView):
    """
    修改密码视图（学生和教师使用）
    需要验证原密码，新密码经 argon2 哈希后存储
    管理员不能使用此视图修改密码
    """
    template_name = 'change_password.html'
    form_class = PasswordChangeForm

    def dispatch(self, request, *args, **kwargs):
        """管理员角色不允许在此页面修改密码"""
        """Admin role cannot change password on this page"""
        if request.user.role == 'admin':
            messages.error(request, '管理员请通过后台管理修改密码')
            return redirect('accounts:home')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """将当前用户传给 PasswordChangeForm"""
        """Pass current user to PasswordChangeForm"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        密码修改成功后的处理
        更新会话哈希，避免用户被登出
        记录审计日志
        """
        user = form.save()
        update_session_auth_hash(self.request, user)
        ip = self.request.META.get('REMOTE_ADDR', 'unknown')
        audit_logger.info(f'密码修改 - 用户名:{user.username} 角色:{user.role} IP:{ip}')
        messages.success(self.request, '密码修改成功！')
        return redirect('accounts:home')

    def form_invalid(self, form):
        """密码修改失败时的处理"""
        """Handle password change failure"""
        messages.error(self.request, '密码修改失败，请检查输入')
        return super().form_invalid(form)

    def get_success_url(self):
        """根据角色返回对应首页"""
        """Return corresponding home page by role"""
        user = self.request.user
        if user.role == 'teacher':
            return reverse_lazy('attendance:teacher_home')
        else:
            return reverse_lazy('attendance:student_home')


class HomeView(View):
    """
    系统首页视图
    根据用户的登录状态和角色重定向到对应页面
    未登录用户跳转到登录页
    """
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        user = request.user
        if user.role == 'admin':
            return redirect('management_app:management_home')
        elif user.role == 'teacher':
            return redirect('attendance:teacher_home')
        else:
            return redirect('attendance:student_home')
