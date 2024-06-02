from django.db.models import Q

from chat.models import Chat


class ChatServices:
    @staticmethod
    def create(data):
        try:
            chat = Chat.objects.create(**data)
            return chat, None
        except Exception as e:
            return None, {"error": f"Exception raised while creating chat. {e}"}
        
    @staticmethod
    def retrieve(data):
        user1_id = data.get('user1_id')
        user2_id = data.get('user2_id')

        try:
            chat = Chat.objects.filter(Q(user1=user1_id , user2=user2_id) | Q(user1=user2_id , user2=user1_id)).first()
            if not chat:
                return None, None
            return chat, None
        except Exception as e:
            return None, {"error": f"Exception raised while retrieving chat. {e}"}