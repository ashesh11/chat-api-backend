from django.urls import path
from chat.views import ChatListView

urlpatterns = [
    path("", ChatListView.as_view(), name='chat-list'),
]