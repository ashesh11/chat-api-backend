import jwt
from django.conf import settings
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from account.models import UserAccount
from channels.db import database_sync_to_async

@database_sync_to_async
def get_user(user_id):
    user = UserAccount.objects.filter(id=user_id).first()
    if not user:
        return AnonymousUser()
    return user


class ChatSocketAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        authorization_header = headers.get(b'authorization')
        if authorization_header:
            try:
                _, token = authorization_header.split(b' ')
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
                user_id = payload['user_id']
                user = await get_user(user_id=user_id)
                
                scope['user'] = user

            except jwt.exceptions.ExpiredSignatureError:
                scope['user'] = AnonymousUser()
            
            except jwt.InvalidSignatureError:
                scope['user'] = AnonymousUser()
            
            
        return await super().__call__(scope, receive, send)