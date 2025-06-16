from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from libs.logging import logger


class BaseViewSet(ModelViewSet):
    """
    基础视图集
    提供标准的REST接口和统一的响应格式
    """
    serializer_class = None

    def get_success_response(self, data=None, message="success", status_code=status.HTTP_200_OK):
        """
        返回成功响应
        """
        response_data = {"status": "success", "message": message, "data": data}
        return Response(response_data, status=status_code)

    def get_error_response(self, message="error", status_code=status.HTTP_400_BAD_REQUEST):
        """
        返回错误响应
        """
        response_data = {"status": "error", "message": message, "data": None}
        return Response(response_data, status=status_code)

    def handle_exception(self, exc):
        """
        统一异常处理
        """
        logger.error(f"Error in {self.__class__.__name__}: {str(exc)}")
        return self.get_error_response(message=str(exc))

    def response_proxy(self, response):
        """
        统一响应格式处理
        """
        if not isinstance(response, Response):
            return response

        data = response.data
        response.data = {
            "status": "success" if response.status_code < 400 else "error",
            "message": self._get_status_message(response.status_code),
            "data": data if response.status_code < 400 else None,
        }
        return response

    def _get_status_message(self, status_code):
        """
        获取状态码对应的消息
        """
        status_messages = {
            status.HTTP_200_OK: "操作成功",
            status.HTTP_201_CREATED: "创建成功",
            status.HTTP_204_NO_CONTENT: "删除成功",
            status.HTTP_400_BAD_REQUEST: "请求参数错误",
            status.HTTP_401_UNAUTHORIZED: "未授权",
            status.HTTP_403_FORBIDDEN: "权限不足",
            status.HTTP_404_NOT_FOUND: "资源不存在",
            status.HTTP_409_CONFLICT: "资源冲突",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "服务器内部错误",
        }
        return status_messages.get(status_code, "未知状态")

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return self.response_proxy(response)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return self.response_proxy(response)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return self.response_proxy(response)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return self.response_proxy(Response(serializer.data))

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return self.response_proxy(response)
