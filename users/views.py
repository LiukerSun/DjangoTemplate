from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.views import BaseViewSet
from .models import User, UserToken
from .serializers import UserSerializer, LoginSerializer, TokenSerializer
from .authentication import generate_token
from libs.decorators import api_log, validate_body_params


class UserViewSet(BaseViewSet):
    """用户视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """根据不同的action设置不同的权限"""
        if self.action in ['create', 'login']:
            return [AllowAny()]
        return super().get_permissions()

    @api_log
    @validate_body_params(['username', 'password', 'email'])
    def create(self, request, *args, **kwargs):
        """注册"""
        return super().create(request, *args, **kwargs)

    @api_log
    @action(detail=False, methods=['post'])
    @validate_body_params(['username', 'password'])
    def login(self, request):
        """登录"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 验证用户
        user = User.objects.filter(username=serializer.validated_data['username']).first()
        if not user or not user.check_password(serializer.validated_data['password']):
            return self.get_error_response("用户名或密码错误", status.HTTP_401_UNAUTHORIZED)

        # 生成token
        token, expires = generate_token(user)
        
        # 返回用户信息和token
        user_data = UserSerializer(user).data
        user_data['token'] = token
        user_data['expires'] = expires
        
        return self.get_success_response(user_data, "登录成功")

    @api_log
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """登出"""
        # 获取当前token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_type, token = auth_header.split(' ')
            # 使token失效
            UserToken.objects.filter(token=token).update(is_active=False)
        
        return self.get_success_response(message="登出成功")

    @api_log
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """获取个人信息"""
        return self.get_success_response(UserSerializer(request.user).data)

    @api_log
    @action(detail=False, methods=['post'])
    @validate_body_params(['old_password', 'new_password'])
    def change_password(self, request):
        """修改密码"""
        user = request.user
        if not user.check_password(request.data['old_password']):
            return self.get_error_response("原密码错误", status.HTTP_400_BAD_REQUEST)
        
        user.set_password(request.data['new_password'])
        user.save()
        
        # 使所有token失效
        UserToken.objects.filter(user=user).update(is_active=False)
        
        # 生成新token
        token, expires = generate_token(user)
        
        return self.get_success_response({
            'token': token,
            'expires': expires
        }, "密码修改成功")
