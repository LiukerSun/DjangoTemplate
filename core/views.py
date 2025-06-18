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

    def get_success_response(
        self, data=None, message="success", status_code=status.HTTP_200_OK
    ):
        """
        返回成功响应
        """
        response_data = {"status": "success", "message": message, "data": data}
        return Response(response_data, status=status_code)

    def get_error_response(
        self, message="error", status_code=status.HTTP_400_BAD_REQUEST
    ):
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
