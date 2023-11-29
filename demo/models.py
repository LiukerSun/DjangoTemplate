from django.db import models


class Device(models.Model):
    id = models.AutoField(primary_key=True)
    device_id = models.CharField(max_length=500, default=None, null=True)
    device_name = models.CharField(max_length=500, unique=True)
