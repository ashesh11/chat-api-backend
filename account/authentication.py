import jwt

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

User = get_user_model()

class AccountJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        This function takes request as input. From request it extracts the authorization token and validates it.
        Authorization token contains the user details trying to login or authenticate.
        User is returned if token is valid.
        """
        
        authorization_header = request.headers.get('Authorization')

        if authorization_header is None:
            raise exceptions.PermissionDenied('No authorization header')
        
        try:
            access_token = authorization_header.split(" ")[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms='HS256'
            )
        
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.PermissionDenied('Expired Signature')
        
        except jwt.InvalidSignatureError:
            raise exceptions.ValidationError('Invalid Signature')

        
        user = User.objects.filter(id=payload['user_id']).first()

        if user is None:
            raise exceptions.NotFound('User not found')
        
        if not user.is_active:
            raise exceptions.PermissionDenied('User is inactive')

        return(user, None)