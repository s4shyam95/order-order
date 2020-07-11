from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$',  views.chat_room, name='game'),
    url(r'^conduct/$',  views.admin_room, name='admin'),
]
