"""
种子数据管理命令
通过 `python manage.py seed_data` 创建测试数据：
- 管理员账号（admin / 12345678）
- 教师账号（teacher1 / 12345678）
- 学生账号（student1~student3 / 12345678）
- 班级（一年级一班、一年级二班）
"""
from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from attendance.models import Class


class Command(BaseCommand):
    help = '创建测试种子数据：管理员、教师、学生账号和班级'

    def handle(self, *args, **options):
        self.stdout.write('开始创建种子数据...')

        # ==================== 创建班级 ====================
        self.stdout.write('创建班级...')
        class1, created1 = Class.objects.get_or_create(
            name='一年级一班',
            defaults={'grade': '一年级'}
        )
        if created1:
            self.stdout.write(self.style.SUCCESS(f'  创建班级：{class1.name}'))
        else:
            self.stdout.write(f'  班级已存在：{class1.name}')

        class2, created2 = Class.objects.get_or_create(
            name='一年级二班',
            defaults={'grade': '一年级'}
        )
        if created2:
            self.stdout.write(self.style.SUCCESS(f'  创建班级：{class2.name}'))
        else:
            self.stdout.write(f'  班级已存在：{class2.name}')

        # ==================== 创建管理员账号 ====================
        self.stdout.write('创建管理员账号...')
        if not CustomUser.objects.filter(username='admin').exists():
            admin = CustomUser.objects.create_superuser(
                username='admin',
                password='12345678',
                email='admin@school.com',
                last_name='系统',
                first_name='管理员',
                role='admin',
                is_active=True,
                is_staff=True,
                is_superuser=True,
            )
            self.stdout.write(self.style.SUCCESS(f'  创建管理员：{admin.username} / 12345678'))
        else:
            self.stdout.write('  管理员账号已存在')

        # ==================== 创建教师账号 ====================
        self.stdout.write('创建教师账号...')
        if not CustomUser.objects.filter(username='teacher1').exists():
            teacher = CustomUser.objects.create_user(
                username='teacher1',
                password='12345678',
                email='teacher1@school.com',
                last_name='张',
                first_name='老师',
                role='teacher',
                teacher_id='T001',
                is_active=True,
            )
            teacher.managed_classes.add(class1, class2)
            self.stdout.write(self.style.SUCCESS(f'  创建教师：{teacher.username} / 12345678（管理 {class1.name}、{class2.name}）'))
        else:
            self.stdout.write('  教师账号已存在')

        # ==================== 创建学生账号 ====================
        self.stdout.write('创建学生账号...')

        students_data = [
            {'username': 'student1', 'student_id': 'S2026001', 'last_name': '李', 'first_name': '明', 'class': class1},
            {'username': 'student2', 'student_id': 'S2026002', 'last_name': '王', 'first_name': '小红', 'class': class1},
            {'username': 'student3', 'student_id': 'S2026003', 'last_name': '赵', 'first_name': '强', 'class': class2},
        ]

        for student_data in students_data:
            if not CustomUser.objects.filter(username=student_data['username']).exists():
                student = CustomUser.objects.create_user(
                    username=student_data['username'],
                    password='12345678',
                    last_name=student_data['last_name'],
                    first_name=student_data['first_name'],
                    role='student',
                    student_id=student_data['student_id'],
                    student_class=student_data['class'],
                    is_active=True,
                )
                self.stdout.write(self.style.SUCCESS(f'  创建学生：{student.username} / 12345678（{student_data["class"].name}）'))
            else:
                self.stdout.write(f'  学生账号 {student_data["username"]} 已存在')

        # ==================== 输出汇总信息 ====================
        self.stdout.write(self.style.SUCCESS('\n种子数据创建完成！'))
        self.stdout.write('=' * 50)
        self.stdout.write('测试账号如下：')
        self.stdout.write(f'  管理员：admin / 12345678')
        self.stdout.write(f'  教师：  teacher1 / 12345678')
        self.stdout.write(f'  学生：  student1 / 12345678（一年级一班）')
        self.stdout.write(f'  学生：  student2 / 12345678（一年级一班）')
        self.stdout.write(f'  学生：  student3 / 12345678（一年级二班）')
        self.stdout.write('=' * 50)
