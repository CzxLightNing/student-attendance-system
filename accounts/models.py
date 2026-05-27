"""
账号管理应用的数据模型定义
包含自定义用户模型 CustomUser，继承 Django 内置的 AbstractUser
增加了角色（role）、学号/工号、班级关联等字段
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    自定义用户模型
    继承 Django AbstractUser 并扩展以下字段：
    - role：用户角色（student/teacher/admin）
    - student_id：学号（仅学生角色使用）
    - teacher_id：工号（仅教师角色使用）
    - student_class：学生所属班级（仅学生角色使用，ForeignKey）
    - managed_classes：教师管理的班级（仅教师角色使用，ManyToMany）
    """
    # 角色选择常量
    # Role choice constants
    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_STUDENT, '学生'),
        (ROLE_TEACHER, '教师'),
        (ROLE_ADMIN, '管理员'),
    ]

    # 角色字段，默认为学生
    # Role field, defaults to student
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_STUDENT,
        verbose_name='角色',
        db_index=True,
    )

    # 学号字段（仅学生角色使用，可为空）
    student_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        verbose_name='学号',
        db_index=True,
    )

    # 工号字段（仅教师角色使用，可为空）
    teacher_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        verbose_name='工号',
    )

    # 学生所属班级（将在 attendance 应用中定义 Class 模型后关联）
    # Student's class (linked to Class model in attendance app)
    # 使用字符串引用延迟绑定，避免循环导入
    # Use string reference for lazy binding, avoid circular import
    student_class = models.ForeignKey(
        'attendance.Class',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='students',
        verbose_name='所属班级',
        db_index=True,
    )

    # 教师管理的班级（多对多关联）
    # Classes managed by teacher (many-to-many)
    managed_classes = models.ManyToManyField(
        'attendance.Class',
        blank=True,
        related_name='teachers',
        verbose_name='管理的班级',
    )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-date_joined']
        # MySQL 兼容：显式指定表名
        # MySQL compatibility: explicit table name
        db_table = 'accounts_customuser'

    def __str__(self):
        """返回用户的可读标识：姓名 + 角色"""
        """Return user readable identifier: name + role"""
        full_name = f"{self.last_name}{self.first_name}"
        display_name = full_name if full_name.strip() else self.username
        role_display = dict(self.ROLE_CHOICES).get(self.role, self.role)
        return f"{display_name}（{role_display}）"

    def is_admin(self):
        """判断用户是否为管理员角色"""
        return self.role == self.ROLE_ADMIN

    def is_teacher(self):
        """判断用户是否为教师角色"""
        return self.role == self.ROLE_TEACHER

    def is_student(self):
        """判断用户是否为学生角色"""
        return self.role == self.ROLE_STUDENT

    @property
    def is_activated(self):
        """判断用户账号是否已被激活（审核通过）"""
        return self.is_active
