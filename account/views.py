from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response

from account.services import UserAccountServices
from account.serializers import UserSignupSerializer, UserLoginSerializer


class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account, errors = UserAccountServices.create(serializer.validated_data)
        if errors:
            return Response(data=errors, status=400)
        serializer = UserSignupSerializer(account)
        return Response(data={"data": serializer.data}, status=200)
    

class UserLoginView(APIView):
    def post(self, request):
        serialier = UserLoginSerializer(data=request.data)
        serialier.is_valid(raise_exception=True)
        account = authenticate(request, **serialier.validated_data)
        if not account:
            return Response(data={"errors": "Unable to login. Invalid credentials."}, status=400)
        return Response(status=200)