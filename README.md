[English](README_EN.md) | 中文

# 学生考勤管理系统

基于 Django 的学生考勤 Web 系统，支持用户注册与登录、教师生成签到码、学生输入签到码签到，并提供管理员、教师、学生三种角色各自的管理与查看功能。

## 仓库地址

- [Gitee](https://gitee.com/chen-zixia666/student-attendance-system)
- [GitHub](https://github.com/CzxLightNing/student-attendance-system)
  > ⚠️ GitHub 仓库为镜像仓库，可能无法及时同步最新推送，请以 Gitee 仓库为准。

## 功能特性

- **多角色管理**：管理员（班级/用户管理、CSV 批量导入）、教师（签到码生成、实时监控、Excel 导出）、学生（签到、历史查看）
- **安全认证**：argon2-cffi 密码哈希、django-axes 登录暴力破解防护、会话安全管理
- **签到实时监控**：教师生成签到码后页面每 3 秒自动轮询，实时展示已签到/未签到学生
- **Excel 考勤导出**：使用 openpyxl 生成规范的考勤表单
- **CSV 批量导入**：支持批量导入班级、学生、教师数据，附带模板下载
- **审计日志**：记录登录、密码修改、数据导入等安全事件
- **NTP 时间同步**：使用阿里云 NTP 服务器确保系统时间准确
- **响应式设计**：基于 Bootstrap 5，兼容桌面端、平板端和移动端

## 技术栈

| 类别       | 技术                               |
| -------- | -------------------------------- |
| 后端框架     | Python 3.10+ / Django 4.2 LTS    |
| 数据库      | SQLite（开发）/ MySQL（生产）            |
| 前端       | HTML5 / CSS3 / ES6 / Bootstrap 5 |
| 密码哈希     | argon2-cffi                      |
| 安全防护     | django-axes                      |
| Excel 导出 | openpyxl                         |
| 生产服务器   | Waitress（多线程 WSGI）             |
| 静态文件服务  | WhiteNoise                        |
| 时间同步     | ntplib（ntp.aliyun.com）           |

## 快速启动

```bash
# 1. 创建并激活虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. （可选）配置环境变量 — SQLite 开箱即用，无需额外配置
copy .env.example .env

# 4. 数据库迁移
python manage.py migrate

# 5. 加载种子数据
python manage.py seed_data

# 6. 启动服务
python manage.py runserver
```

浏览器访问 `http://127.0.0.1:8000/`

## 生产环境部署

项目内置 **Waitress** 生产级 WSGI 服务器 + **WhiteNoise** 静态文件服务：

```bash
# 收集静态文件
python manage.py collectstatic --noinput

# 启动生产服务器
python server.py
```

可在 `.env` 中配置：`WAITRESS_HOST`、`WAITRESS_PORT`、`WAITRESS_THREADS`、`WAITRESS_CHANNEL_TIMEOUT`。

## 测试账号

| 角色  | 用户名         | 密码         |
| --- | ----------- | ---------- |
| 管理员 | **`admin`** | `12345678` |
| 教师  | `teacher1`  | `12345678` |
| 学生  | `student1`  | `12345678` |

## 项目结构

```
student-attendance-system/
├── manage.py
├── server.py                  # 生产服务器入口
├── requirements.txt
├── config/                  # Django 项目配置
├── accounts/                # 账号管理应用
├── attendance/              # 签到考勤应用
├── management_app/          # 管理面板应用
├── templates/               # HTML 模板
├── static/                  # 静态资源
├── media/                   # 临时导出文件
└── logs/                    # 审计日志
```

## 许可证

本项目基于 MIT 许可证开源，详见 [LICENSE](LICENSE) 文件。
