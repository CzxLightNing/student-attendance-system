import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
# Load environment variables from .env file
load_dotenv()

# 项目根目录路径
# Project root directory path
BASE_DIR = Path(__file__).resolve().parent.parent

# 从环境变量读取运行模式，默认开发模式
# Read runtime mode from env, defaults to development
ENVIRONMENT = os.getenv('DJANGO_ENV', 'development')

# Django 签名密钥，生产环境必须从 .env 读取
# Django signing key; must be set via .env in production
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key-change-in-production-12345678')

# 调试模式：开发环境开启，生产环境必须关闭
# Debug mode: enabled in dev, must be disabled in production
if ENVIRONMENT == 'production':
    DEBUG = False
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
else:
    DEBUG = True
    ALLOWED_HOSTS = ['*']

# 注册 Django 应用
# Django registered apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方应用
    # Third-party apps
    'axes',  # 登录暴力破解防护
    # 自定义应用
    # Custom apps
    'accounts.apps.AccountsConfig',
    'attendance.apps.AttendanceConfig',
    'management_app.apps.ManagementAppConfig',
]

# Django 中间件配置
# Django middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # django-axes 中间件，需放在 AuthenticationMiddleware 之后
    # django-axes middleware, must be placed after AuthenticationMiddleware
    'axes.middleware.AxesMiddleware',
]

# 根 URL 配置模块
# Root URL configuration module
ROOT_URLCONF = 'config.urls'

# 模板配置
# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI 应用入口
# WSGI application entry point
WSGI_APPLICATION = 'config.wsgi.application'

# 数据库配置：默认使用 SQLite，无需任何环境变量
# Database config: SQLite by default, no env vars needed
# 如需切换到 MySQL，在 .env 中设置 DATABASE_ENGINE=django.db.backends.mysql 并填写相关凭据
# To switch to MySQL, set DATABASE_ENGINE=django.db.backends.mysql in .env with credentials
DATABASE_ENGINE = os.getenv('DATABASE_ENGINE', '')
if DATABASE_ENGINE == 'django.db.backends.mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DATABASE_NAME', 'attendance_db'),
            'USER': os.getenv('DATABASE_USER', 'root'),
            'PASSWORD': os.getenv('DATABASE_PASSWORD', ''),
            'HOST': os.getenv('DATABASE_HOST', 'localhost'),
            'PORT': os.getenv('DATABASE_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# 自定义用户模型
AUTH_USER_MODEL = 'accounts.CustomUser'

# 认证后端配置（包含 django-axes 的认证后端）
# Auth backend config (includes django-axes backend)
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# 密码哈希算法配置：优先使用 Argon2，其次使用 Django 内置算法
# Password hashing config: prefer Argon2, fall back to Django built-in
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# 密码验证器配置
# Password validator configuration
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 国际化配置：中文语言 + 上海时区
# I18n config: Chinese language + Asia/Shanghai timezone
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# 静态文件配置
# Static files configuration
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise 静态文件服务配置
# WhiteNoise static file serving config
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_AUTOREFRESH = DEBUG

# 媒体文件配置（用于临时导出文件）
# Media files config (for temporary export files)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 默认主键字段类型
# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 登录/登出 URL 配置
# Login / Logout URL config
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Messages 框架的标签映射，用于 Bootstrap 5 样式
# Messages framework tag mapping for Bootstrap 5 styles
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# ==================== django-axes 登录失败锁定配置 ====================
# ==================== django-axes Login Failure Lockout Config ====================
AXES_FAILURE_LIMIT = 5                      # 失败次数阈值
AXES_COOLOFF_TIME = 0.5                     # 锁定冷却时间（小时），0.5 表示 30 分钟
AXES_LOCKOUT_PARAMETERS = ['username', 'ip_address']  # 同时按用户名和 IP 锁定
AXES_RESET_ON_SUCCESS = True                # 登录成功后重置失败计数
AXES_LOCKOUT_CALLABLE = None                # 不显示特定锁定原因

# ==================== 会话安全配置 ====================
# ==================== Session Security Config ====================
SESSION_COOKIE_AGE = 7200                    # 会话超时时间（秒），2 小时
SESSION_EXPIRE_AT_BROWSER_CLOSE = True      # 关闭浏览器后清除会话
SESSION_SAVE_EVERY_REQUEST = True            # 每次请求更新会话过期时间

# ==================== 生产环境安全配置 ====================
# ==================== Production Security Config ====================
if ENVIRONMENT == 'production':
    # 强制 HTTPS 重定向
    # Force HTTPS redirect
    SECURE_SSL_REDIRECT = True
    # Cookie 仅通过 HTTPS 传输
    # Cookies only sent over HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # 防止 JavaScript 读取 Session Cookie
    # Prevent JavaScript from reading session cookie
    SESSION_COOKIE_HTTPONLY = True
    # 限制跨站请求中 Cookie 的发送
    # Restrict cookie sending in cross-site requests
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SAMESITE = 'Lax'
    # HSTS 头部配置（浏览器强制 HTTPS，有效期 1 年）
    # HSTS header config (force HTTPS, 1 year duration)
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# 安全 HTTP 响应头配置
# Security HTTP response headers config
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# ==================== 审计日志配置 ====================
# ==================== Audit Logging Config ====================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'audit_format': {
            'format': '[{asctime}] [{levelname}] {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'audit_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'audit.log'),
            'maxBytes': 1024 * 1024 * 10,  # 单个日志文件最大 10MB
            'backupCount': 5,              # 保留 5 个旧日志文件
            'formatter': 'audit_format',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'audit_format',
        },
    },
    'loggers': {
        'audit': {
            'handlers': ['audit_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
