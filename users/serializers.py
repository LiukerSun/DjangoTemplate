from rest_framework import serializers
from core.serializers import BaseModelSerializer
from .models import User, UserToken


class UserSerializer(BaseModelSerializer):
    """用户序列化器"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'password', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['is_active']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    username = serializers.CharField()
    password = serializers.CharField()


class TokenSerializer(BaseModelSerializer):
    """Token序列化器"""
    class Meta:
        model = UserToken
        fields = ['token', 'expires', 'is_active', 'created_at'] 