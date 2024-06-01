import os
import jwt
import datetime
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()


def generate_access_token(user):
    """
    Takes user instance and returns a token.
    This token is to be provided in every request header to access an authorized page.
    """
    access_token_payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=int(os.getenv('ACCESS_TOKEN_VALIDITY_PERIOD'))),
        "iat": datetime.datetime.utcnow()
    }
    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY
    )
    return access_token


def generate_refresh_token(user):
    """
    Takes user instance and returns a token.
    This token is to be used to generate new access_token in case access_token validity period is expired.
    """
    refresh_token_payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=int(os.getenv('REFRESH_TOKEN_VALIDITY_PERIOD'))),
        "iat": datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY
    )
    return refresh_token