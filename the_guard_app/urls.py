from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^rasp/(?P<rasp_serial>[A-Za-z0-9]+)/$', views.rasp_view, name='rasp'),
    url('', views.index, name='index'),
]
