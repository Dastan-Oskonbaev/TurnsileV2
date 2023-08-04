from django.urls import re_path

from apps.pool.consumers import TurnstileConsumer

websocket_urlpatterns = [
    re_path(r"ws/(?P<room_name>\w+)/$", TurnstileConsumer.as_asgi()),
]
