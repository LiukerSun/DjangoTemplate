# 使用官方Python运行时作为父镜像
FROM python:3.11.13
# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Shanghai

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p /app/logs /app/media /app/staticfiles

# 设置环境变量以确保静态文件收集正确工作
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONPATH=/app

# 安装 drf-yasg 的静态文件
RUN pip install --no-cache-dir --force-reinstall drf-yasg

# 收集静态文件
RUN python manage.py collectstatic --noinput --clear

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "4", "config.wsgi:application"] 