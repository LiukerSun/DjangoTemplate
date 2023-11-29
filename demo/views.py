from rest_framework.response import Response
from demo import models, serializers, exceptions
from libs.custom_logger import logger
from libs.custom_functions import (
    api_log,
)
from libs.baseView import BaseViewSet


class DeviceViewSet(BaseViewSet):
    model = models.Device
    queryset = model.objects.all()
    serializer_class = serializers.DeviceSerializer

    @api_log
    def list(self, request, *args, **kwargs):
        queryset = self.model.objects
        serializer = self.get_serializer(queryset, many=True)
        response = Response(serializer.data)
        logger.info(serializer.data)
        response = self.response_proxy(response)
        return response
