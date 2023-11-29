from rest_framework import serializers
from demo import models


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device
        fields = (
            "id",
            "device_id",
            "device_name",
        )

    def to_representation(self, instance):
        data = {
            "id": instance.id,
            "device_id": instance.device_id,
            "device_name": instance.device_name,
        }
        return data
