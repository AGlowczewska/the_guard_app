from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^v1/camera_address', views.get_test_address),
    url(r'^v1/devices/add', views.register_rasp),
    url(r'^v1/devices', views.get_devices_for_owner),
    url(r'^v1/devices/assign', views.assign_device_to_owner),
]