from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from django.utils import timezone
from channels.db import database_sync_to_async

# from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from asgiref.sync import async_to_sync
from django.conf import LazySettings
settings = LazySettings()


# @database_sync_to_async
# def close_connections():
#     close_old_connections()


# @database_sync_to_async
# def get_user(token_key):
#     try:
#         return Token.objects.get(key=token_key)
#     except Exception as e:
#         print(e)
#         return AnonymousUser()


class TokenAuthMiddleware:
    """
    Token [Querystring/Header] authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        # close_connections()
        query_string = parse_qs(scope['query_string'])
        headers = dict(scope['headers'])
        if b'token' in query_string:
            try:
                token_key = query_string[b'token'][0].decode()
                # print(token_key)
                # token = get_user(token_key)
                # print(token)
                scope['token'] = token_key
                scope['user'] = AnonymousUser()
            except Exception as e:
                print(e)
                scope['user'] = AnonymousUser()
        elif b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Token':
                    token = async_to_sync(Token.objects.get(key=token_key))
                    scope['user'] = token.user
            except Exception:
                scope['user'] = AnonymousUser()
        else:
            pass

        return self.inner(scope)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
