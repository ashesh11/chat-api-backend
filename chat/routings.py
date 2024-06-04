from chat import consumers
from django.urls import path


websocket_urlpatterns = [
    path("chat/<int:user2_id>/messages/", consumers.ChatMessageConsumer.as_asgi()),
]