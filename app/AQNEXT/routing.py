# from channels.routing import route
# from YBUTILS.wsConsumers import *

from channels.routing import ProtocolTypeRouter
from django.urls import path
from django.urls import re_path

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from YBUTILS.websocketTokenAuth import TokenAuthMiddlewareStack

from YBUTILS.wsConsumers import JSONConsumer, ChatConsumer
print("_______________ROUTING__________________")
application = ProtocolTypeRouter({
    "websocket": TokenAuthMiddlewareStack(
        URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            re_path(r'room/user/(?P<room_name>\w+)$', JSONConsumer),
            re_path(r'room/(?P<room_name>\w+)$', JSONConsumer),
            re_path(r'room/(?P<room_name>\w+)/(?P<user_name>\w+)$', JSONConsumer)
        ]),
    ),
})

from .pinebooSettings import *
