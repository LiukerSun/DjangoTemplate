from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel


class User(AbstractUser, BaseModel):
    """自定义用户模型"""
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    )
    
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True, verbose_name="手机号")
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name="邮箱")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="头像")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O', verbose_name="性别")
    birthday = models.DateField(null=True, blank=True, verbose_name="生日")
    introduction = models.TextField(max_length=500, null=True, blank=True, verbose_name="简介")
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="最后登录IP")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    is_staff = models.BooleanField(default=False, verbose_name="是否为员工")
    
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ["-date_joined"]
        
    def __str__(self):
        return self.username or self.phone or self.email


class UserToken(BaseModel):
    """用户Token"""
    TOKEN_TYPE_CHOICES = (
        ('access', '访问令牌'),
        ('refresh', '刷新令牌'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokens", verbose_name="用户")
    token = models.CharField(max_length=500, verbose_name="Token")
    token_type = models.CharField(max_length=10, choices=TOKEN_TYPE_CHOICES, default='access', verbose_name="Token类型")
    expires = models.DateTimeField(verbose_name="过期时间")
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    device = models.CharField(max_length=200, null=True, blank=True, verbose_name="设备信息")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP地址")
    user_agent = models.TextField(null=True, blank=True, verbose_name="User Agent")
    
    class Meta:
        verbose_name = "用户Token"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
        
    def __str__(self):
        return f"{self.user.username} - {self.token_type} - {self.expires}"
        
    def save(self, *args, **kwargs):
        if not self.pk:  # 如果是新创建的token
            # 使相同类型的旧token失效
            UserToken.objects.filter(
                user=self.user,
                token_type=self.token_type,
                is_active=True
            ).update(is_active=False)
        super().save(*args, **kwargs)
