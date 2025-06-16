from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """
    基础模型序列化器
    提供通用的序列化功能
    """
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        abstract = True
