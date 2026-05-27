"""
账号管理应用的权限装饰器和 Mixin
提供基于角色的视图访问控制
"""
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func=None, login_url=None):
    """
    管理员角色装饰器
    仅允许 role 为 'admin' 的用户访问被装饰的视图
    """
    def check_admin(user):
        return user.is_authenticated and user.role == 'admin'

    actual_decorator = user_passes_test(
        check_admin,
        login_url=login_url,
        redirect_field_name=None,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def teacher_required(view_func=None, login_url=None):
    """
    教师角色装饰器
    仅允许 role 为 'teacher' 的用户访问被装饰的视图
    """
    def check_teacher(user):
        return user.is_authenticated and user.role == 'teacher'

    actual_decorator = user_passes_test(
        check_teacher,
        login_url=login_url,
        redirect_field_name=None,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def student_required(view_func=None, login_url=None):
    """
    学生角色装饰器
    仅允许 role 为 'student' 的用户访问被装饰的视图
    """
    def check_student(user):
        return user.is_authenticated and user.role == 'student'

    actual_decorator = user_passes_test(
        check_student,
        login_url=login_url,
        redirect_field_name=None,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


class AdminRequiredMixin(UserPassesTestMixin):
    """
    管理员角色 Mixin（用于 Class-Based Views）
    仅允许管理员角色的用户访问视图
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

    def handle_no_permission(self):
        messages.error(self.request, '您没有访问此页面的权限')
        return redirect('home')


class TeacherRequiredMixin(UserPassesTestMixin):
    """
    教师角色 Mixin（用于 Class-Based Views）
    仅允许教师角色的用户访问视图
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'teacher'

    def handle_no_permission(self):
        messages.error(self.request, '您没有访问此页面的权限')
        return redirect('home')


class StudentRequiredMixin(UserPassesTestMixin):
    """
    学生角色 Mixin（用于 Class-Based Views）
    仅允许学生角色的用户访问视图
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'student'

    def handle_no_permission(self):
        messages.error(self.request, '您没有访问此页面的权限')
        return redirect('home')
