"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from chat.routings import websocket_urlpatterns
from chat.middleware import ChatSocketAuthMiddleware



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

get_asgi_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application,
        "websocket": ChatSocketAuthMiddleware(
            AllowedHostsOriginValidator(
                AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
            )
        )
    }
)