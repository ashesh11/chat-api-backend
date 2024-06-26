from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response

from account.services.account import UserAccountServices
from account.services.token import BlacklistTokenServices
from account.serializers import UserSignupSerializer, UserLoginSerializer, UserListSerializer
from account.utils import generate_access_token, generate_refresh_token


class UserSignupView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'erros': serializer.errors}, status=400)
        account, errors = UserAccountServices.create(serializer.validated_data)
        if errors:
            return Response(data=errors, status=400)
        serializer = UserSignupSerializer(account)
        return Response(data={"data": serializer.data}, status=200)
    

class UserLoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        """
        Takes login credential and send access_token and refresh_token in response.
        Also adds refresh token in cookie.
        """
        serialier = UserLoginSerializer(data=request.data)
        if not serialier.is_valid():
            return Response(data={'errors': serialier.errors}, status=400)
        account = authenticate(request, **serialier.validated_data)
        if not account:
            return Response(data={"errors": "Unable to login. Invalid credentials."}, status=400)
        
        access_token = generate_access_token(account)
        refresh_token = generate_refresh_token(account)

        data = {'access_token': access_token, 'refresh_token': refresh_token}
        response = Response(data={"data":data}, status=202)
        response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)

        return response
    

class UserLogoutView(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
        _, error = BlacklistTokenServices.add_to_blacklist(token)
        if error:
            return Response(data=error, status=400)
        return Response(data={"data": "User logged out"})
    

class UserAccountListView(APIView):
    def get(self, request):
        accounts, error = UserAccountServices.list_active_users()
        if error:
            return Response(data=error, status=400)
        
        # Excluding self in the chat list
        accounts = accounts.exclude(id=request.user.id)

        serializer = UserListSerializer(accounts, many=True)
        return Response(data={"data": serializer.data})