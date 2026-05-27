# 贡献指南

感谢你对学生考勤管理系统的关注！本文档将帮助你了解如何参与项目贡献。

## 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [环境搭建](#环境搭建)
- [开发工作流](#开发工作流)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [测试指南](#测试指南)
- [文档规范](#文档规范)

## 行为准则

- 尊重所有贡献者，保持友好和专业的交流氛围
- 提出建设性意见，聚焦于问题本身而非个人
- 帮助新贡献者熟悉项目和流程

## 如何贡献

### 报告 Bug

1. 确认 bug 尚未被报告过
2. 提供清晰的描述：复现步骤、预期行为、实际行为
3. 标注环境信息：操作系统、Python 版本、浏览器版本
4. 附上相关截图或错误日志

### 提交功能请求

1. 描述你希望添加的功能
2. 说明该功能的适用场景和价值
3. 如果可能，描述你期望的实现方式

### 提交代码

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/your-feature`)
3. 编写代码并确保符合规范
4. 在本地充分测试
5. 提交 Pull Request，描述变更内容

## 环境搭建

> **🚫 严禁在全局 Python 环境中直接安装依赖！**

```bash
# 1. 克隆仓库
git clone <repository-url>
cd student-attendance-system

# 2. 创建并激活虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量（可选，SQLite 开箱即用）
copy .env.example .env

# 5. 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 6. 加载种子数据
python manage.py seed_data

# 7. 启动开发服务器
python manage.py runserver
```

### 测试账号

| 角色   | 用户名       | 密码         |
|--------|-------------|-------------|
| 管理员 | `admin`     | `12345678`  |
| 教师   | `teacher1`  | `12345678`  |
| 学生   | `student1`  | `12345678`  |

## 开发工作流

### 分支策略

- `main` — 稳定发布分支
- `develop` — 开发主分支
- `feature/*` — 新功能开发
- `fix/*` — Bug 修复
- `docs/*` — 文档更新

### 开发前检查清单

- [ ] 已在最新 `develop` 分支上创建特性分支
- [ ] 理解要修改的模块及其关联依赖
- [ ] 阅读 `AGENTS.md` 了解项目整体架构和约定

### 开发后检查清单

- [ ] `python manage.py check` 无报错
- [ ] 在浏览器中手动测试受影响页面
- [ ] 未破坏已有功能（回归测试）
- [ ] 代码符合规范（见下方）
- [ ] 相关文档已同步更新

## 代码规范

### Python 代码规范

| 规则       | 说明                                                              |
|-----------|--------------------------------------------------------------------|
| 编码风格    | 严格遵循 [PEP8](https://peps.python.org/pep-0008/)                 |
| 缩进       | 4 个空格，禁止使用 Tab                                             |
| 行宽       | 不超过 120 字符                                                    |
| 注释       | 所有模块、类、函数均需添加规范的中文注释，说明代码逻辑、用途、参数、返回值等 |
| 视图       | 优先使用 Django Class-Based Views (CBV)，管理面板可适当使用函数视图    |
| 权限       | 需登录的视图使用 `LoginRequiredMixin`，角色权限使用自定义 Mixin 或装饰器  |

### 前端代码规范

| 规则     | 说明                                                                        |
|----------|---------------------------------------------------------------------------|
| 注释     | HTML、CSS、JavaScript 均需添加规范的中文注释                                   |
| JS 语法  | 使用 ES6，不依赖任何前端 JS 框架（React、Vue、jQuery 等）                         |
| CSS 框架 | Bootstrap 5 仅用于 CSS 样式和响应式布局，不使用 Bootstrap JS 组件                |
| AJAX     | 使用原生 `fetch` API                                                         |
| 响应式   | 兼容桌面端（≥1200px）、平板端（≥768px）、移动端（<768px）                        |

### 命名规范

| 语言       | 风格         | 示例                  |
|-----------|-------------|----------------------|
| Python 变量/函数 | `snake_case`  | `get_student_list`   |
| Python 类名     | `PascalCase`  | `StudentCheckinView` |
| Python 常量     | `UPPER_CASE`  | `LOGIN_URL`          |
| JavaScript 变量/函数 | `camelCase`  | `handleGenerate`     |
| CSS 类名        | `kebab-case`  | `.card-header`       |

### URL 命名空间

项目使用 Django URL 命名空间区分应用路由：

| 应用             | 命名空间               |
|-----------------|------------------------|
| accounts        | `accounts:`            |
| attendance      | `attendance:`          |
| management_app  | `management_app:`      |

在模板 `{% url %}` 和视图中 `reverse()` / `redirect()` / `reverse_lazy()` 必须使用命名空间前缀。

### 安全检查

- 密码使用 `argon2-cffi` 哈希，严禁明文存储
- 所有 POST 请求包含 CSRF token
- AJAX 请求 header 中携带 `X-CSRFToken`
- 文件上传限制：`.csv` 扩展名、`text/csv` MIME、最大 5MB
- 时间同步使用 `ntplib` 从 `ntp.aliyun.com` 获取，不可依赖本地系统时间

## 提交规范

推荐使用语义化提交信息格式：

```
<type>: <简短描述>

<详细说明（可选）>
```

### 类型 (type)

| 类型       | 说明                       |
|-----------|---------------------------|
| `feat`    | 新功能                      |
| `fix`     | Bug 修复                    |
| `docs`    | 文档变更                     |
| `style`   | 代码风格/格式调整（不影响逻辑）  |
| `refactor`| 代码重构                     |
| `perf`    | 性能优化                     |
| `test`    | 测试相关                     |
| `chore`   | 构建/工具/依赖变更            |

### 示例

```
feat: 新增签到码过期提醒功能

教师在签到码即将过期时会收到页面通知。
```

```
fix: 修复教师端轮询使用错误签到码ID导致不更新
```

## 测试指南

### 开发服务器测试

```bash
python manage.py runserver
# 浏览器访问 http://127.0.0.1:8000/
```

### 生产服务器测试

```bash
python manage.py collectstatic --noinput
python server.py
# 浏览器访问 http://127.0.0.1:8000/
```

### 系统检查

```bash
# 基础检查
python manage.py check

# 部署安全检查
python manage.py check --deploy
```

### 功能测试策略

- 用至少两种角色账号登录，验证权限隔离
- 测试核心流程：注册 → 登录 → 生成签到码 → 签到 → 查看历史 → 导出 Excel
- 测试边界条件：空表单、过期签到码、重复签到、无权限访问

## 文档规范

- 所有文档使用 Markdown 格式
- 中文文档为主，英文文档通过 `README_EN.md` 同步维护
- API 文档使用中文注释
- 更新功能时，同步更新 `CHANGELOG.md`
- 项目结构和技术说明收束在 `AGENTS.md`
