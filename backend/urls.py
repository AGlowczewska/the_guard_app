from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^v1/camera_address', views.get_test_address),
    url(r'^v1/devices/add', views.register_rasp),
    url(r'^v1/devices/get', views.get_devices_for_owner),
    url(r'^v1/devices/assign', views.assign_device_to_owner),
    url(r'^v1/notification', views.notification),
    url(r'^v1/fcmTokenUpdate', views.fcmTokenUpdate),
    url(r'^v1/devices/changeRaspName', views.changeRaspName),
    url(r'^v1/devices/changeIsArmed', views.changeIsArmed),
    url(r'^v1/devices/notifications', views.getNotifications),
    url(r'^v1/PIRnotification', views.notificationPIR),
]
