from account.services.account import UserAccountServices
from chat.services import ChatServices
from chat.models import Message

class ChatSocketTools:
    def __init__(self, scope):
        self.scope = scope
        self.user1= scope['user']
        self.user2_id = scope['url_route']['kwargs']['user2_id']

    
    def verify_users(self):
        user1 = self.scope['user']
        if user1.is_anonymous:
            return False
        
        _, error = UserAccountServices.retrieve_active_user(self.user2_id)
        if error:
            return False
        
        return True

    def get_or_create_chat(self):
        data = {'user1_id': self.user1.id, 'user2_id':self.user2_id}
        chat, error = ChatServices.retrieve(data=data)
        if error:
            return None, error
        
        if not chat:
            chat, error = ChatServices.create(data=data)
            if error:
                return None, error
            
        return chat, None
    
    def retrieve_chat_conversation(self, chat_id):
        messages = Message.objects.filter(chat_id=chat_id).order_by('timestamp')
        conversation = []
        for message in messages:
            conversation.append({"user": message.sender.email, "message": message.content})
        return conversation, None
    
    def add_message(self, data):
        Message.objects.create(**data)