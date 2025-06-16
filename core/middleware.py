import time
import json
import logging
from django.conf import settings

logger = logging.getLogger('django')

class RequestLogMiddleware:
    """请求日志中间件"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # 记录请求信息
        request_data = {
            'path': request.path,
            'method': request.method,
            'query_params': request.GET.dict(),
            'client_ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
        }
        
        # 如果是POST/PUT/PATCH请求，记录请求体
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                request_data['body'] = json.loads(request.body) if request.body else None
            except json.JSONDecodeError:
                request_data['body'] = 'Invalid JSON'
                
        logger.info(f'Request: {json.dumps(request_data)}')
        
        response = self.get_response(request)
        
        # 记录响应信息
        response_data = {
            'status_code': response.status_code,
            'path': request.path,
            'method': request.method,
        }
        
        logger.info(f'Response: {json.dumps(response_data)}')
        
        return response


class ResponseTimeMiddleware:
    """响应时间中间件"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        response['X-Response-Time'] = f'{duration:.3f}s'
        
        # 如果响应时间超过1秒，记录警告日志
        if duration > 1:
            logger.warning(
                f'Slow response detected: {request.path} - {duration:.3f}s'
            )
            
        return response 