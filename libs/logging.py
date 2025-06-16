import os
import sys
from loguru import logger
from pathlib import Path
from django.conf import settings

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 日志文件路径
LOG_PATH = BASE_DIR / 'logs'

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

# 日志轮转配置
logger.configure(
    handlers=[
        # 控制台输出
        {
            "sink": sys.stdout,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                     "<level>{level: <8}</level> | "
                     "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                     "<level>{message}</level>",
            "level": "INFO" if not settings.DEBUG else "DEBUG",
        },
        # INFO级别日志文件
        {
            "sink": LOG_PATH / "info.log",
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
                     "{name}:{function}:{line} - {message}",
            "level": "INFO",
            "rotation": "1 day",
            "retention": "7 days",
            "compression": "zip",
            "encoding": "utf-8",
        },
        # ERROR级别日志文件
        {
            "sink": LOG_PATH / "error.log",
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
                     "{name}:{function}:{line} - {message}",
            "level": "ERROR",
            "rotation": "1 day",
            "retention": "30 days",
            "compression": "zip",
            "encoding": "utf-8",
        },
    ],
)

# 移除默认的handler
logger.remove()

# 添加上下文信息
logger = logger.bind(service="django-template")

# 导出logger实例
__all__ = ['logger']
