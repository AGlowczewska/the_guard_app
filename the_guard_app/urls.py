from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^rasp/(?P<rasp_serial>[A-Za-z0-9]+)/$', views.rasp_view, name='rasp'),
    url(r'change_armed_status/(?P<rasp_serial>[A-Za-z0-9]+)/$', views.change_armed_status, name='change_armed_status'),
    url(r'notifications/(?P<rasp_serial>[A-Za-z0-9]+)/$', views.notifications, name='notifications'),
    url(r'rename/(?P<rasp_serial>[A-Za-z0-9]+)/$', views.rename, name='rename'),
    url(r'^connect/$', views.connect_rasp, name='connect'),
    url('', views.index, name='index'),
]
