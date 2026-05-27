# 学生考勤管理系统 - 项目技术说明文档

## 项目简介
基于 Django 的学生考勤 Web 系统，支持用户注册与登录、教师生成签到码、学生输入签到码签到，并提供管理员、教师、学生三种角色各自的管理与查看功能。

## 技术栈
- **后端**: Python 3.10+, Django 4.2 LTS
- **数据库**: SQLite（开发环境），设计兼容 MySQL 迁移
- **前端**: 原生 HTML5、CSS3、JavaScript（ES6），Bootstrap 5 响应式栅格系统
- **认证**: Django 内置认证系统 + argon2-cffi 密码哈希
- **安全**: django-axes 登录防护、会话安全、CSRF 保护
- **时间同步**: ntplib 从 NTP 服务器获取时间
- **导出**: openpyxl 生成 Excel 考勤表单

## 目录结构
```
student-attendance-system/
├── manage.py                  # Django 管理入口
├── requirements.txt           # Python 依赖清单
├── .env.example               # 环境变量配置模板
├── .gitignore                 # Git 忽略规则
├── AGENTS.md                  # 本文件，项目技术说明
├── config/                    # Django 项目配置
│   ├── settings.py            # 主配置文件（含安全、数据库、日志等）
│   ├── urls.py                # 根 URL 路由
│   ├── wsgi.py                # WSGI 入口
│   └── asgi.py                # ASGI 入口
├── accounts/                  # 账号管理应用
│   ├── models.py              # CustomUser 自定义用户模型
│   ├── views.py               # 登录、注册、登出、修改密码视图
│   ├── urls.py                # 账号相关 URL 路由
│   └── decorators.py          # 角色权限装饰器
├── attendance/                # 签到考勤应用
│   ├── models.py              # Class、AttendanceCode、AttendanceRecord 模型
│   ├── views.py               # 签到、签到码管理、考勤详情、导出视图
│   └── urls.py                # 考勤相关 URL 路由
├── management_app/            # 管理面板应用
│   ├── views.py               # 班级管理、用户管理、考勤总览视图
│   └── urls.py                # 管理面板 URL 路由
├── templates/                 # HTML 模板文件
├── static/                    # 静态资源（Bootstrap CSS/JS）
├── media/                     # 临时导出文件目录
└── logs/                      # 应用日志目录
```

## 环境要求
- Python 3.10 或更高版本
- pip 包管理器
- 虚拟环境（推荐使用 venv）

## 快速启动

> **🚫 严禁在全局 Python 环境中直接安装依赖！必须先创建并激活虚拟环境。**

```bash
# 1. 创建并激活虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. 安装项目依赖
pip install -r requirements.txt

# 3. （可选）复制并配置环境变量 — SQLite 无需额外配置，可直接跳过此步
copy .env.example .env

# 4. 执行数据库迁移
python manage.py makemigrations
python manage.py migrate

# 5. 加载种子数据（创建测试账号和班级）
python manage.py seed_data

# 6. 启动开发服务器
python manage.py runserver

# 7. 访问系统
# 打开浏览器访问 http://127.0.0.1:8000/
# 测试账号：
#   管理员：admin / 12345678
#   教师：  teacher1 / 12345678
#   学生：  student1 / 12345678
```

## 代码规范

### Python 代码规范
- 严格遵循 PEP8 编码规范
- 所有模块、类、函数、关键代码块必须添加规范的中文注释
- 注释应说明代码逻辑、函数用途、参数含义、返回值等
- 使用 4 个空格缩进，不使用 Tab
- 行宽不超过 120 字符

### 前端代码规范
- HTML、CSS、JavaScript 代码同样需要添加规范的中文注释
- JavaScript 使用 ES6 语法
- 不依赖任何前端 JS 框架（如 React、Vue、jQuery），仅使用原生 JavaScript
- Bootstrap 5 仅用于 CSS 样式，不使用 Bootstrap JS 组件

### 命名规范
- Python 变量/函数：snake_case（小写字母 + 下划线）
- Python 类名：PascalCase（首字母大写）
- Python 常量：UPPER_CASE（全大写 + 下划线）
- JavaScript 变量/函数：camelCase（驼峰命名）
- CSS 类名：kebab-case（小写字母 + 连字符）
- HTML/CSS 类名遵循 Bootstrap 5 命名约定

## 关键约定

### 视图实现方式
- 优先使用 Django Class-Based Views（CBV）作为主要视图实现方式
- 管理面板的部分视图可使用函数视图
- 所有需要登录的视图必须使用 LoginRequiredMixin 或 @login_required 装饰器
- 角色权限检查使用自定义 Mixin 或装饰器

### 后端约定
- 密码哈希：使用 argon2-cffi，严禁明文存储密码
- 时间同步：使用 ntplib 从 ntp.aliyun.com 获取时间，不可依赖本地系统时间
- 安全防护：django-axes 登录失败锁定、会话超时 2 小时
- 审计日志：记录登录、密码修改、数据导入等安全相关事件
- 所有 POST 请求包含 CSRF token，AJAX 请求 header 中带 X-CSRFToken

### 前端约定
- Bootstrap 5 仅用于 CSS 样式和响应式布局
- 所有动态交互使用原生 JavaScript 实现（不依赖 Bootstrap JS 或 jQuery）
- AJAX 请求使用 fetch API
- 响应式设计兼容桌面端（≥1200px）、平板端（≥768px）、移动端（<768px）

### 数据库约定
- 当前使用 SQLite，模型设计需兼容后续 MySQL 迁移
- 所有 CharField 显式指定 max_length
- 所有外键显式设置 on_delete 行为
- DateTimeField 使用 auto_now_add 和 auto_now 时注意 MySQL 兼容性
- 为关键查询字段添加索引

### CSV 导入安全
- 文件扩展名必须为 .csv
- MIME 类型必须为 text/csv
- 单文件大小不超过 5MB
- 上传文件使用时间戳重命名，防止路径遍历攻击
