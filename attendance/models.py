"""
签到考勤应用的数据模型定义
包含班级（Class）、签到码（AttendanceCode）、签到记录（AttendanceRecord）模型
所有模型设计遵循 MySQL 兼容规范
"""
from django.db import models
from django.conf import settings


class Class(models.Model):
    """
    班级模型
    存储学校班级的基本信息
    """
    # 班级名称（如"一年级一班"），全局唯一
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='班级名称',
    )
    # 年级（如"一年级"）
    grade = models.CharField(
        max_length=50,
        verbose_name='年级',
    )
    # 创建时间
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
    )

    class Meta:
        verbose_name = '班级'
        verbose_name_plural = '班级'
        ordering = ['grade', 'name']
        # MySQL 兼容：显式指定表名
        db_table = 'class_group'

    def __str__(self):
        """返回班级的名称标识"""
        return self.name


class AttendanceCode(models.Model):
    """
    签到码模型
    由教师生成，关联到特定班级，有过期时间和生效状态
    同一班级同一时间只能有一个有效签到码
    """
    # 所属班级
    class_group = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name='所属班级',
        db_index=True,
    )
    # 4 位数字签到码
    code = models.CharField(
        max_length=4,
        verbose_name='签到码',
    )
    # 创建签到码的教师
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='创建教师',
    )
    # 创建时间
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
    )
    # 课程开始时间（用于迟到判定，可选）
    course_start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='课程开始时间',
    )
    # 过期时间
    expires_at = models.DateTimeField(
        verbose_name='过期时间',
        db_index=True,
    )
    # 是否有效（教师可手动失效）
    is_active = models.BooleanField(
        default=True,
        verbose_name='是否有效',
        db_index=True,
    )

    class Meta:
        verbose_name = '签到码'
        verbose_name_plural = '签到码'
        ordering = ['-created_at']
        # MySQL 兼容：显式指定表名
        db_table = 'attendance_attendancecode'
        # 联合索引：加速按班级查询有效签到码
        indexes = [
            models.Index(fields=['class_group', 'is_active'], name='idx_class_active'),
            models.Index(fields=['code', 'is_active'], name='idx_active_code'),
        ]

    def __str__(self):
        """返回签到码的可读标识"""
        return f"签到码 {self.code} - {self.class_group.name}"


class AttendanceRecord(models.Model):
    """
    签到记录模型
    记录学生的一次签到操作，关联到具体的签到码
    同一个学生对同一个签到码只能有一条记录
    """
    # 签到学生
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='签到学生',
        db_index=True,
    )
    # 对应的签到码
    attendance_code = models.ForeignKey(
        AttendanceCode,
        on_delete=models.CASCADE,
        verbose_name='对应签到码',
        db_index=True,
    )
    # 签到时间戳
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='签到时间',
    )
    # 签到状态：正常 / 迟到 / 缺勤
    STATUS_NORMAL = '正常'
    STATUS_LATE = '迟到'
    STATUS_ABSENT = '缺勤'

    STATUS_CHOICES = [
        (STATUS_NORMAL, '正常'),
        (STATUS_LATE, '迟到'),
        (STATUS_ABSENT, '缺勤'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NORMAL,
        verbose_name='签到状态',
    )

    class Meta:
        verbose_name = '签到记录'
        verbose_name_plural = '签到记录'
        ordering = ['-timestamp']
        # MySQL 兼容：显式指定表名
        db_table = 'attendance_attendancerecord'
        # 联合唯一约束：一个学生对一个签到码只能签到一次
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'attendance_code'],
                name='uq_student_code',
            ),
        ]
        indexes = [
            models.Index(fields=['student', 'timestamp'], name='idx_student_timestamp'),
        ]

    def __str__(self):
        """返回签到记录的可读标识"""
        return f"{self.student.last_name}{self.student.first_name} - {self.attendance_code.code} - {self.status}"
