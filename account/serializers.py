from rest_framework import serializers


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()