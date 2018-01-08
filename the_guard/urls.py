"""the_guard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from users import views as users_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', users_views.login_user, name='login'),
    url(r'^logout/$', users_views.logout_user, name='logout'),
    url(r'^signup/$', users_views.signup, name='signup'),
    url('', include('the_guard_app.urls')),
    url('the_guard', include('the_guard_app.urls')),
]

