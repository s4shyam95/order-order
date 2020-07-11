from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$',  views.chat_room, name='game'),
    url(r'^conduct/$',  views.admin_room, name='conduct'),
    url(r'^admin/', admin.site.urls, name='admin'),
]
