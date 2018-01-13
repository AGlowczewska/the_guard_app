from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^v1/camera_address/', views.get_test_address),
    url(r'^v1/add_raspberry/', views.register_rasp),
    url(r'^v1/get_camera_owner/$', views.get_rasps),
    url(r'^v1/connect/', views.connect_rasp_with_user),
]