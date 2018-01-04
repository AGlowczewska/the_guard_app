from django.conf.urls import url
from . import views

urlpatterns = [
    url('users', views.get_users, name='users'),
    url('', views.index, name='index'),
]
