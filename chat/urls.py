from django.urls import path

from chat.views import ChatView, MessageView

urlpatterns = [
    path("", ChatView.as_view(), name='chat-list'),
    path("<int:chat_id>/messages/", MessageView.as_view(), name='chat-messages')
]