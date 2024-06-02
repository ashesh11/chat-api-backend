from rest_framework.views import APIView
from rest_framework.response import Response

from chat.serializers import ChatCreateSerializer, ChatDetailSerializer
from chat.services import ChatServices

class ChatView(APIView): 
    def post(self, request):
        data = request.data
        data['user1_id'] = request.user.id
        print(data)

        serializer = ChatCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        chat, error = ChatServices.retrieve(data=serializer.validated_data)
        if error:
            return Response(data=error, status=400)
        
        if not chat:
            chat, error = ChatServices.create(data=serializer.validated_data)
            if error:
                return Response(data=error, status=400)
        
        serializer = ChatDetailSerializer(chat)
            
        return Response(data={"data": serializer.data}, status=200)


class MessageView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass