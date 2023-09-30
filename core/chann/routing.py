from django.urls import re_path

from core.chann.consumers import Consumer

websocket_urlpatterns = [
    re_path("ws/chann/", Consumer.as_asgi()),
    #re_path(r'ws/chann/(?P<room_name>\w+)/$',Consumer.as_asgi()),
]