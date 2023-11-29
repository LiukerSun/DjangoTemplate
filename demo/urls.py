from django.urls import path
from . import views

device = views.DeviceViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

urlpatterns = [
    path(r"device/", device),
]
