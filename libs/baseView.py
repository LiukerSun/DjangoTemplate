from rest_framework import viewsets, status
from rest_framework.response import Response


class BaseViewSet(viewsets.ModelViewSet):
    """
    Custome base ViewSet class needed to be inherited
    """

    model = None
    serializer_class = None
    current_user = None

    def response_proxy(self, response):
        """
        A proxy method that add custom detail message in response.data.
        :param response:
        :return:
        """
        if response.data:
            data = response.data
            response.data = dict()
            response.data["data"] = data
        else:
            response.data = dict()
        if response.status_code == status.HTTP_200_OK:
            response.data["detail"] = "请求成功"
        elif response.status_code == status.HTTP_201_CREATED:
            response.data["detail"] = "创建成功"
        elif response.status_code == status.HTTP_204_NO_CONTENT:
            response.data["detail"] = "删除成功"
        elif response.status_code == status.HTTP_202_ACCEPTED:
            response.data["detail"] = "更新成功"
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            response.data["detail"] = "资源不存在"
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            response.data["detail"] = "不存在"
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response = self.response_proxy(response)
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response = self.response_proxy(response)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response = self.response_proxy(response)
        return response

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response = Response(serializer.data)
        response = self.response_proxy(response)
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response = self.response_proxy(response)
        return response
