from chat import consumers
from django.urls import path


websocket_urlpatterns = [
    path("chat/messages/", consumers.ChatMessageConsumer.as_asgi()),
]