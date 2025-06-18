"""
Custom exception handler for django exceptions and some custom exceptions.
"""

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError


def custom_exception_handler(exc, context):
    """
    自定义异常处理
    """
    # 生成统一的错误信息
    def _build_error(msg: str, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(
            {
                "status": "error",
                "message": msg,
                "data": None,
            },
            status=status_code,
        )

    response = exception_handler(exc, context)
    
    if response is None:
        # 非 DRF 抛出的异常
        if isinstance(exc, Http404):
            response = _build_error("资源不存在", status.HTTP_404_NOT_FOUND)
        elif isinstance(exc, PermissionDenied):
            response = _build_error("权限不足", status.HTTP_403_FORBIDDEN)
        elif isinstance(exc, IntegrityError):
            response = _build_error("数据完整性错误", status.HTTP_400_BAD_REQUEST)
        else:
            response = _build_error("服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # DRF 内置异常
        message = response.data.get("detail", "请求错误")
        response = _build_error(message, response.status_code)
    
    return response


class BusinessException(APIException):
    """业务异常基类"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '业务处理失败'
    default_code = 'business_error'
    
    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
            
        self.detail = {
            'code': code,
            'message': str(detail)
        }


class ResourceNotFoundError(BusinessException):
    """资源不存在异常"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = '资源不存在'
    default_code = 'not_found'


class ValidationError(BusinessException):
    """数据验证异常"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '数据验证失败'
    default_code = 'validation_error'


class PermissionError(BusinessException):
    """权限异常"""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = '权限不足'
    default_code = 'permission_denied'
