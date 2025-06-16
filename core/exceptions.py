"""
Custom exception handler for django exceptions and some custom exceptions.
"""

from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError


def custom_exception_handler(exc, context):
    """
    自定义异常处理
    """
    response = exception_handler(exc, context)
    
    if response is None:
        if isinstance(exc, Http404):
            data = {
                'code': 404,
                'message': '资源不存在',
                'detail': str(exc)
            }
            response = Response(data, status=status.HTTP_404_NOT_FOUND)
            
        elif isinstance(exc, PermissionDenied):
            data = {
                'code': 403,
                'message': '权限不足',
                'detail': str(exc)
            }
            response = Response(data, status=status.HTTP_403_FORBIDDEN)
            
        elif isinstance(exc, IntegrityError):
            data = {
                'code': 400,
                'message': '数据完整性错误',
                'detail': str(exc)
            }
            response = Response(data, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            data = {
                'code': 500,
                'message': '服务器内部错误',
                'detail': str(exc)
            }
            response = Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        # 处理DRF内置异常
        data = {
            'code': response.status_code,
            'message': response.data.get('detail', '请求错误'),
            'detail': response.data
        }
        response.data = data
    
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
