import jwt

from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response

from account.services import UserAccountServices
from account.serializers import UserSignupSerializer, UserLoginSerializer
from account.utils import generate_access_token, generate_refresh_token


class UserSignupView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
        serialier.is_valid(raise_exception=True)
        account = authenticate(request, **serialier.validated_data)
        if not account:
            return Response(data={"errors": "Unable to login. Invalid credentials."}, status=400)
        
        access_token = generate_access_token(account)
        refresh_token = generate_refresh_token(account)

        data = {'access_token': access_token, 'refresh_token': refresh_token}
        response = Response(data={"data":data}, status=202)
        response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)

        return response
    

class RefreshTokenView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        """
        This view function takes request as input. Request contains refresh_token.
        Refresh token is checked for its validity and new access token is returned in reponse if valid.
        """
        # Get the refresh token from the request data
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response(data={"errors": "key 'refresh_token' not provided or empty value provided"})
        try:
            # Decode the refresh token using the Django secret key
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms='HS256'
            )

        except jwt.ExpiredSignatureError:
            return Response(data={"errors": "Refresh token validity period expired"} ,status=400)
        
        except jwt.InvalidSignatureError:
            return Response(data={"errors": "Invalid refresh token"}, status=400)
        
        # Retrieve the user associated with the refresh token
        user, errors = UserAccountServices.retrieve_active_user(user_id=payload.get("user_id"))

        if errors:
            return Response(data=errors, status=404)

        # Generate a new access token and return it in the response
        access_token = generate_access_token(user)
        return Response(data={"data": {"access_token": access_token}}, status=201)