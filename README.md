# Django Template Project

这是一个基于 Django + DRF 的现代化项目模板，集成了常用功能和最佳实践，经过系统性代码审查和优化。

---

## ✨ 特色功能

- ⛓ 统一的 **JWT** 认证与刷新机制
- 🗂️ **PostgreSQL** 数据库存储，连接池与长连接优化
- 🚦 **DRF** + 自定义响应渲染器，统一 API 返回格式
- 🎛️ 多中间件支持：请求日志、性能监控、静态文件、CORS 等
- 🧩 内置 **软删除** 与时间戳基类模型，支持审计字段
- 📚 **Swagger** / **ReDoc** 在线 API 文档，支持 Token 调试
- ⚡ 本地内存缓存 + 装饰器级缓存封装
- 🔐 速率限制、参数校验、装饰器式日志记录
- 🐳 一条命令启动的 **Docker** 化部署

---

## 📂 目录结构

```
backend/
├── config/              # Django 全局配置
│   ├── settings.py      # 设置文件（按环境变量动态配置）
│   ├── urls.py          # 根路由
│   └── wsgi.py          # WSGI 入口
├── core/                # 核心抽象 & 中间件
│   ├── exceptions.py    # 全局异常处理
│   ├── middleware.py    # 请求日志 & 性能监控
│   ├── models.py        # BaseModel 软删除实现
│   ├── pagination.py    # 自定义分页
│   ├── renderers.py     # 统一响应渲染器
│   └── views.py         # 通用视图基类
├── users/               # 用户与认证模块
│   ├── authentication.py# JWT 认证实现
│   ├── models.py        # 自定义用户、Token
│   └── views.py         # 用户接口
├── libs/                # 通用工具库
│   ├── decorators.py    # 日志/限流/缓存等装饰器
│   └── logging.py       # Loguru 日志配置
├── Dockerfile           # 后端镜像构建脚本
├── docker-compose.yml   # 容器编排
├── env.template         # 环境变量模板
├── manage.py            # Django 管理脚本
└── requirements.txt     # Python 依赖清单
```

---

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone <your-repo-url> LiveControl && cd LiveControl/backend
```

### 2. 使用 Docker（推荐）
```bash
# 复制并修改环境变量
cp env.template .env
# 一键启动
docker-compose up -d --build
# 首次启动后初始化数据库
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

访问接口文档：
- Swagger: http://localhost:8000/swagger/
- ReDoc:   http://localhost:8000/redoc/

### 3. 本地开发
```bash
python -m venv venv && source venv/bin/activate  # Windows 使用 venv\Scripts\activate
pip install -r requirements.txt
cp env.template .env
python manage.py migrate && python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

> 提示：在 `DEBUG=True` 模式下，浏览器可访问 `/swagger/` 调试接口。

---

## ⚙️ 关键配置

所有可调参数均通过 **环境变量** 注入，详见 `env.template`：

| 变量 | 说明 | 默认 |
| --- | --- | --- |
| `DEBUG` | 是否开启调试模式 | `True` |
| `DB_*` | 数据库连接信息 | - |
| `SECRET_KEY` | Django 密钥 | - |
| `JWT_EXPIRATION_DELTA` | 访问令牌有效期（天） | `7` |
| `JWT_REFRESH_EXPIRATION_DELTA` | 刷新令牌有效期（天） | `30` |
| `ALLOWED_HOSTS` | 允许的主机名 | `*` |
| `CORS_ALLOWED_ORIGINS` | 允许跨域的地址 | - |

配置生效顺序：`.env` > 系统环境变量 > settings 默认值。

---

## 🔧 常用命令

```bash
# 生成迁移文件
docker-compose exec web python manage.py makemigrations
# 应用迁移
docker-compose exec web python manage.py migrate
# 收集静态资源
docker-compose exec web python manage.py collectstatic --noinput
# 进入容器终端
docker-compose exec web bash
```

---

## 🛰️ 部署到生产

1. 设置 `DEBUG=False`，并配置 `ALLOWED_HOSTS`、`SECRET_KEY` 等关键环境变量。
2. 推荐使用 Nginx 反向代理至容器内 `gunicorn`（已在 `docker-compose.yml` 中预配置）。
3. 使用持久化卷挂载 `staticfiles/` 与 `media/` 目录。
4. 如需横向扩容，可在 compose / k8s 中增加 `web` 实例并共享数据库与缓存。

---

## 📖 API 快速索引

| 方法 | 路径 | 描述 |
| ---- | ---- | ---- |
| `POST` | `/api/users/` | 用户注册 |
| `POST` | `/api/users/login/` | 用户登录 |
| `POST` | `/api/users/logout/` | 用户登出 |
| `GET` | `/api/users/profile/` | 获取个人信息 |
| `POST` | `/api/users/change_password/` | 修改密码 |

更多接口请查看在线文档。

---

## 📜 许可证

本项目使用 **MIT License**，详见 `LICENSE` 文件。