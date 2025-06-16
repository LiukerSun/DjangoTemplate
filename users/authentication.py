from datetime import datetime, timedelta
import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from .models import User, UserToken


class JWTAuthentication(authentication.BaseAuthentication):
    """JWT认证类"""
    
    def authenticate(self, request):
        # 获取token
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            # 分离token
            auth_type, token = auth_header.split(' ')
            if auth_type.lower() != 'bearer':
                return None

            # 验证token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('user_id')
            if not user_id:
                raise exceptions.AuthenticationFailed('Invalid token')

            # 获取用户
            user = User.objects.filter(id=user_id, is_active=True).first()
            if not user:
                raise exceptions.AuthenticationFailed('User not found')

            # 验证token是否在数据库中且有效
            token_obj = UserToken.objects.filter(
                user=user,
                token=token,
                is_active=True,
                expires__gt=datetime.now()
            ).first()
            if not token_obj:
                raise exceptions.AuthenticationFailed('Token expired or invalid')

            return (user, token)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))

    def authenticate_header(self, request):
        return 'Bearer'


def generate_token(user):
    """生成JWT token"""
    # Token过期时间设置为7天
    expires = datetime.now() + timedelta(days=7)
    
    # 创建JWT payload
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': expires.timestamp()
    }
    
    # 生成token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    # 保存token到数据库
    UserToken.objects.create(
        user=user,
        token=token,
        expires=expires,
        is_active=True
    )
    
    return token, expires 