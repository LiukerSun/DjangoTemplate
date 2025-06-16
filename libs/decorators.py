"""
API装饰器模块
提供API请求日志记录和参数验证等功能
"""

from functools import wraps
from rest_framework.response import Response
from libs.logging import logger
import time
import functools
from django.core.cache import cache
from django.conf import settings
from core.exceptions import BusinessException


def api_log(func):
    """
    API调用日志装饰器
    记录请求的路径、方法、数据等信息，自动过滤敏感信息
    """

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        # 过滤掉敏感信息
        safe_headers = {
            k: v
            for k, v in request.headers.items()
            if k.lower() not in ["authorization", "cookie"]
        }
        safe_data = {
            k: "******" if k.lower() in ["password", "token"] else v
            for k, v in request.data.items()
        }

        logger.info(
            f"API调用 - {request.method} {request.path}\n"
            f"Query参数: {request.GET}\n"
            f"请求数据: {safe_data}\n"
            f"请求头: {safe_headers}"
        )

        return func(self, request, *args, **kwargs)

    return wrapper


def validate_body_params(required_params):
    """
    请求参数校验装饰器
    验证请求体中是否包含所有必需的参数

    Args:
        required_params (list): 必需参数列表

    Returns:
        function: 装饰器函数

    Example:
        @validate_body_params(['username', 'password'])
        def my_view(self, request):
            # 参数验证通过后的处理逻辑
            pass
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            missing_params = [
                param for param in required_params if param not in request.data
            ]
            if missing_params:
                return Response(
                    {
                        "status": "error",
                        "message": f"缺少必需参数: {', '.join(missing_params)}",
                        "data": None,
                    },
                    status=400,
                )
            return view_func(self, request, *args, **kwargs)

        return wrapper

    return decorator


def rate_limit(key_prefix, limit=60, period=60):
    """
    速率限制装饰器
    :param key_prefix: 缓存key前缀
    :param limit: 限制次数
    :param period: 时间周期(秒)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            # 获取用户IP
            ip = request.META.get('REMOTE_ADDR')
            # 缓存key
            cache_key = f"rate_limit:{key_prefix}:{ip}"
            # 获取当前访问次数
            count = cache.get(cache_key, 0)
            
            if count >= limit:
                raise BusinessException(
                    detail=f"请求过于频繁，请{period}秒后再试",
                    code="rate_limit"
                )
            
            # 增加访问次数
            if count == 0:
                cache.set(cache_key, 1, period)
            else:
                cache.incr(cache_key)
                
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator


def cache_response(timeout=300, key_prefix='view'):
    """
    缓存响应装饰器
    :param timeout: 缓存时间(秒)
    :param key_prefix: 缓存key前缀
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            # 生成缓存key
            cache_key = f"cache:{key_prefix}:{request.path}:{request.query_params}"
            # 尝试获取缓存
            response_data = cache.get(cache_key)
            
            if response_data is not None:
                return Response(response_data)
            
            # 执行视图函数
            response = func(self, request, *args, **kwargs)
            # 设置缓存
            cache.set(cache_key, response.data, timeout)
            
            return response
        return wrapper
    return decorator


def log_time(description=""):
    """
    记录函数执行时间装饰器
    :param description: 描述信息
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            print(f"{description} 执行时间: {end_time - start_time:.3f}秒")
            return result
        return wrapper
    return decorator


def validate_params(*params):
    """
    参数验证装饰器
    :param params: 需要验证的参数名列表
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            data = request.data if request.method in ['POST', 'PUT', 'PATCH'] else request.query_params
            
            for param in params:
                if param not in data:
                    raise BusinessException(
                        detail=f"缺少参数: {param}",
                        code="missing_parameter"
                    )
                    
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator
