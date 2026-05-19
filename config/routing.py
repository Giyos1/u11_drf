from django.urls import re_path
from chat import consumers

websocket_urlpatterns = [
    # ws://localhost/ws/chat/general/
    re_path(
        r'ws/chat/(?P<room_name>\w+)/$',
        consumers.ChatConsumer.as_asgi()
    ),
    re_path(
        r'ws/notifications/$',
        consumers.NotificationConsumer.as_asgi()
    ),
]
