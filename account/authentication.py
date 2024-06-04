import jwt

from django.conf import settings

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from account.services.account import UserAccountServices
from account.services.token import BlacklistTokenServices


class AccountJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        This function takes request as input. From request it extracts the authorization token and validates it.
        Authorization token contains the user details trying to login or authenticate.
        User is returned if token is valid.
        """
        
        authorization_header = request.headers.get('Authorization')

        if authorization_header is None:
            raise exceptions.PermissionDenied({"error": "No authorization header"})
        
        try:
            access_token = authorization_header.split(" ")[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms='HS256'
            )
        
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.PermissionDenied({"error": "Access token validity period expired"})
        
        except jwt.InvalidSignatureError:
            raise exceptions.ValidationError({"error": "Invalid access token"})
        
        except jwt.exceptions.DecodeError:
            raise exceptions.PermissionDenied({"error": "Invalid access token. Not enough segments"})
        
        _, errors = BlacklistTokenServices.check_if_blacklisted(token=access_token)
        
        if errors:
            raise exceptions.PermissionDenied(errors)

        user, errors = UserAccountServices.retrieve_active_user(user_id=payload.get('user_id'))

        if errors:
            exceptions.PermissionDenied(errors)
        
        return(user, None)