# Changelog

## [Unreleased]

### Added
- 新增 Waitress 多线程 WSGI 生产服务器支持，通过 `python server.py` 启动
- 新增 WhiteNoise 中间件，生产环境自动提供静态文件服务
- 新增 `server.py` 生产服务器入口脚本
- 新增 `.env.example` 中 Waitress 配置项（`WAITRESS_HOST` / `WAITRESS_PORT` / `WAITRESS_THREADS` / `WAITRESS_CHANNEL_TIMEOUT`）
- 新增 `README.md` / `README_EN.md` 语言切换链接
- 新增 `README.md` / `README_EN.md` / `AGENTS.md` 生产环境部署章节

### Fixed
- 修复所有模板和视图中 URL 命名空间缺失导致的 `NoReverseMatch` 错误
- 修复 `class_form.html` 中 `edit_class` 变量不存在导致的 `VariableDoesNotExist` 错误
- 修复 `user_form.html` 中 `edit_user` 为 `None` 时模板访问其属性导致的崩溃
- 修复 `UserCreateView` 和 `UserEditView` 中缺失 `edit_user` / `form_data` / `errors` 上下文变量
- 修复 `LogoutView` 的 `next_page` 缺少命名空间前缀
- 修复 `AdminRequiredMixin` / `TeacherRequiredMixin` / `StudentRequiredMixin` 中 `redirect('home')` 缺少 `accounts:` 前缀
- 修复 `TeacherGenerateCodeView` 返回 JSON 中缺少 `id` 字段导致教师端轮询失败
- 修复 `management_app/views.py` 因 PowerShell 操作导致的 UTF-8 编码损坏

### Changed
- 所有 `reverse()` / `reverse_lazy()` / `redirect()` / `{% url %}` 均已使用命名空间前缀（`accounts:` / `attendance:` / `management_app:`）
- 技术栈文档更新：加入 Waitress、WhiteNoise
- `requirements.txt` 新增 `waitress>=3.0.0`、`whitenoise>=6.0`
- `.gitignore` 中 `staticfiles/` 仍保持排除

## [0.1.0] - 2026-05-27

### Added
- 初始项目搭建：Django 4.2 LTS + SQLite + Bootstrap 5
- 用户注册/登录/登出，argon2-cffi 密码哈希
- 管理员、教师、学生三种角色权限体系
- 管理员：班级管理、用户管理、CSV 批量导入、考勤总览
- 教师：签到码生成与失效、实时签到监控（3 秒轮询）、Excel 考勤导出
- 学生：签到码签到、签到历史查看
- django-axes 登录暴力破解防护
- ntplib NTP 时间同步
- openpyxl Excel 导出
- 响应式设计，兼容桌面端、平板端、移动端
- 种子数据管理命令 `python manage.py seed_data`
