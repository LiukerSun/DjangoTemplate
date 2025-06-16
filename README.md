# Django Template Project

这是一个基于 Django + DRF 的现代化项目模板，集成了常用功能和最佳实践，经过系统性代码审查和优化。

## ✨ 特性

- 🎯 基于 Django 5.0.1 和 DRF 3.14.0
- 🔐 完整的JWT认证系统（含token管理）
- 🗄️ PostgreSQL 数据库支持
- ⚡ 本地内存缓存系统
- 📚 Swagger/ReDoc API 文档
- 📝 结构化日志系统 (loguru)
- 🐳 完整 Docker 支持
- 🌐 CORS 跨域支持
- 🛡️ 安全中间件配置
- 👤 扩展的自定义用户模型
- 🗑️ 软删除功能
- ⏱️ API 限流和性能监控
- 📊 请求/响应时间监控
- 🎨 静态文件优化 (WhiteNoise)
- 🔄 统一API响应格式
- 🛠️ 丰富的自定义装饰器

## 🚀 快速开始

### 使用 Docker（推荐）

1. **克隆项目**
```bash
git clone git@github.com:LiukerSun/DjangoTemplate.git
cd DjangoTemplate
```

2. **配置环境变量**
```bash
cp env.template .env
# 编辑 .env 文件，填写必要的配置
```

3. **启动服务**
```bash
docker-compose up -d --build
```

4. **数据库初始化**
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

5. **查看API文档**
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

### 本地开发

1. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境**
```bash
cp env.template .env
# 编辑 .env 文件，配置数据库等信息
```

4. **数据库设置**
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. **启动开发服务器**
```bash
python manage.py runserver
```

## 📁 项目结构

```
DjangoTemplate/
├── config/                 # Django 项目配置
│   ├── __init__.py
│   ├── settings.py        # 主配置文件
│   ├── urls.py           # 主路由配置
│   └── wsgi.py           # WSGI 配置
├── core/                  # 核心应用
│   ├── __init__.py
│   ├── exceptions.py     # 自定义异常处理
│   ├── middleware.py     # 自定义中间件
│   ├── models.py         # 基础模型（软删除等）
│   ├── pagination.py     # 分页组件
│   ├── serializers.py    # 基础序列化器
│   └── views.py          # 基础视图集
├── users/                 # 用户管理应用
│   ├── __init__.py
│   ├── apps.py           # 应用配置
│   ├── authentication.py # JWT认证实现
│   ├── migrations/       # 数据库迁移文件
│   ├── models.py         # 用户模型和Token模型
│   ├── serializers.py    # 用户序列化器
│   ├── urls.py           # 用户路由
│   └── views.py          # 用户视图集
├── libs/                  # 工具库
│   ├── decorators.py     # 自定义装饰器（日志、限流等）
│   └── logging.py        # 日志配置
├── logs/                 # 日志文件目录
│   └── .gitkeep         # 保持目录存在
├── requirements.txt      # Python 依赖
├── Dockerfile           # Docker 镜像配置
├── docker-compose.yml   # Docker Compose 配置
├── env.template         # 环境变量模板
└── manage.py           # Django 管理脚本
```

## 🔧 核心功能

### 认证系统
- **JWT Token 认证**: 支持access token和refresh token
- **自定义用户模型**: 扩展字段包含手机号、邮箱、头像、性别等
- **Token管理**: 自动失效旧token，支持多设备登录跟踪
- **认证装饰器**: 提供便捷的认证和权限控制

### 中间件系统
- `RequestLogMiddleware`: 详细的请求日志记录，自动过滤敏感信息
- `ResponseTimeMiddleware`: 响应时间监控，慢请求告警
- `WhiteNoiseMiddleware`: 高效的静态文件服务
- `CorsMiddleware`: 完整的跨域请求支持

### 基础模型和视图
- **BaseModel**: 提供软删除、时间戳等通用功能
- **BaseViewSet**: 统一的API响应格式，自动异常处理
- **BaseModelSerializer**: 统一的序列化器基类

### 装饰器系统
- `@api_log`: API调用日志记录
- `@validate_body_params`: 请求参数验证
- `@rate_limit`: API限流保护
- `@cache_response`: 响应缓存
- `@log_time`: 性能监控

### 缓存系统
项目使用 Django 内置的本地内存缓存，适合：
- 🖥️ 单机部署场景
- 🔬 开发和测试环境
- 📦 中小型项目
- ⚡ 快速原型开发

缓存配置项：
- `TIMEOUT`: 缓存过期时间（默认300秒）
- `MAX_ENTRIES`: 最大缓存条目数（默认1000）
- `CULL_FREQUENCY`: 清除频率（默认1/3）

## 📖 API 文档

项目集成了两种API文档格式：

### Swagger UI
- 开发环境: http://localhost:8000/swagger/
- 交互式API测试界面
- 支持Bearer Token认证

### ReDoc
- 开发环境: http://localhost:8000/redoc/
- 美观的API文档展示
- 更好的阅读体验

### 主要API端点

- `POST /api/users/`: 用户注册
- `POST /api/users/login/`: 用户登录
- `POST /api/users/logout/`: 用户登出
- `GET /api/users/profile/`: 获取个人信息
- `POST /api/users/change_password/`: 修改密码

## 🚢 部署指南

### Docker 部署（推荐）

```bash
# 构建并启动服务
docker-compose up -d --build

# 数据库初始化
docker-compose exec web python manage.py migrate

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f web

# 停止服务
docker-compose down
```

### 生产环境部署

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **配置环境变量**
```bash
# 设置生产环境变量
export DEBUG=False
export SECRET_KEY=your-secret-key
export DB_NAME=your-db-name
# ... 其他环境变量
```

3. **数据库迁移**
```bash
python manage.py migrate
```

4. **创建超级用户**
```bash
python manage.py createsuperuser
```

5. **启动 Gunicorn**
```bash
gunicorn --bind 0.0.0.0:8000 --workers 4 --threads 4 config.wsgi:application
```

## 💻 开发指南

### 创建新应用
```bash
python manage.py startapp your_app_name
# 记得在 settings.py 的 INSTALLED_APPS 中添加新应用
```

### 数据库操作
```bash
# 创建迁移文件
python manage.py makemigrations

# 查看迁移计划
python manage.py showmigrations

# 应用迁移
python manage.py migrate

# 回滚迁移
python manage.py migrate app_name migration_name
```

### 代码质量检查
```bash
# 安装开发工具
pip install black isort flake8

# 代码格式化
black .
isort .

# 代码检查
flake8 .
```

### 添加新的API端点

1. **在models.py中定义模型**
2. **在serializers.py中创建序列化器**
3. **在views.py中继承BaseViewSet创建视图**
4. **在urls.py中配置路由**
5. **使用装饰器添加日志和验证**


## 📜 许可证

[MIT License](LICENSE)