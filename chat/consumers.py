import sys
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from chat.utils import ChatSocketTools


def handle_errors(self, text_data):
    self.accept()
    self.send(text_data=json.dumps(text_data))
    self.close()
    sys.exit(1)

class ChatMessageConsumer(WebsocketConsumer):
    def connect(self):
        self.tools = ChatSocketTools(scope=self.scope)

        if not self.tools.verify_users():
            handle_errors(self, {'error': 'unverified users'})

        self.chat, error = self.tools.get_or_create_chat()
        if error:
            handle_errors(self, error)

        self.chatroom_name = self.chat.id

        conversation, error = self.tools.retrieve_chat_conversation(chat_id=self.chat.id)
        if error:
            handle_errors(self, error)


        async_to_sync(self.channel_layer.group_add)(
            f'chatroom{self.chat.id}', self.channel_name
        )

        self.accept()
        self.send(text_data=json.dumps(conversation))


    def receive(self, text_data):
        data = {'chat_id': self.chat.id, 'sender_id': self.scope['user'].id, 'content': text_data}

        self.tools.add_message(data=data)

        async_to_sync(self.channel_layer.group_send)(
            f'chatroom{self.chat.id}', {
                'type': 'message_handler',
                'chat_id': self.chat.id
            }
        )

    def disconnect(self, *args, **kwargs):
        pass

    def message_handler(self, data):
        chat_id = data['chat_id']
        conversation = self.tools.retrieve_chat_conversation(chat_id)
        self.send(text_data=json.dumps(conversation))