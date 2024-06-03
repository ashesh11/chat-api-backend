import json
from channels.generic.websocket import WebsocketConsumer


class ChatMessageConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data='connection established')

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))

    def disconnect(self, *args, **kwargs):
        pass