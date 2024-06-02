from rest_framework import serializers

class ChatCreateSerializer(serializers.Serializer):
    user1_id = serializers.IntegerField()
    user2_id = serializers.IntegerField()


class ChatDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()