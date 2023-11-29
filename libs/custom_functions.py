from libs.custom_logger import logger
from demo import models, exceptions
from rest_framework.response import Response

import jwt


def decode_jwt(token):
    try:
        return jwt.decode(token, "123456", algorithms=["HS256"])
    except:
        raise exceptions.HTTP403


# 日志打印装饰器。记录接口调用信息。
def api_log(func):
    def wrapper(self, request, *args, **kwargs):
        logger.info(
            rf"""
                    path:{request.path}
                    method:{request.method}
                    data: {request.data}
                    header:{request.headers}
                    get:{request.GET}
                    """
        )
        result = func(self, request, *args, **kwargs)
        return result

    return wrapper


# 请求参数校验装饰器。
def validate_body_params(required_params):
    def decorator(view_func):
        def wrapper(self, request, *args, **kwargs):
            # 验证请求体中是否包含必需的参数
            missing_params = [
                param for param in required_params if param not in request.data
            ]
            if missing_params:
                return Response(
                    {"error": f'body缺少参数: {", ".join(missing_params)}'},
                    status=400,
                )
            # 如果所有参数都存在，继续执行视图函数
            return view_func(self, request, *args, **kwargs)

        return wrapper

    return decorator
