from channels.generic.websocket import JsonWebsocketConsumer
import json
from asgiref.sync import async_to_sync
# from portal.tasks import sec3
# from AQNEXT.celery import app
from YBUTILS.DbRouter import get_current_user
from channels.generic.websocket import WebsocketConsumer
try:
    from pineboolib.qsa import qsa
except:
    pass


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

class MyConsumer(JsonWebsocketConsumer):

    def connect(self):
        print(self.scope["user"])
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name

        # # Join room group
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )

        # self.accept()
        # try:
        #     roomName = self.scope['url_route']['kwargs']['room_name']
        # except Exception:
        #     roomName = "events"
        print(self.channel_name)
        async_to_sync(self.channel_layer.group_add)(
            "events",
            self.channel_name
        )
        print("???????????")
        self.accept()
        # async_to_sync(self.channel_layer.group_send)(
        #     "events",
        #     {
        #         "type": "on.login",
        #         "content": "conexion",
        #      },
        # )

    def disconnect(self, close_code):
        print('inside EventConsumer disconnect()')
        print("Closed websocket with code: ", close_code)
        async_to_sync(self.channel_layer.group_discard)(
            'events',
            self.channel_name
        )
        self.close()

    def envia(channel, grupo, mensaje):
        async_to_sync(channel.group_send)(
            "events",
            {
                "type": "on.login",
                "content": "enviamosdesdeapi",
             },
        )

    def receive_json(self, content, **kwargs):
        print('inside EventConsumer receive_json()')
        print("Received event: {}".format(content))
        print("____________", self.channel_name)
        # sec3.delay(content, self.channel_name)
        # MyConsumer.envia(self, "events", "desdeap")
        # obj = qsa.from_project("formAPI").entry_point("get", "articulos", "edulopez", {"params": {"filter":'["pvp","gt",1]'}}, "get")
        # print(obj)
        self.send_json(content)

    def on_alarm(self, event):
        print('inside EventConsumer events_alarm()')
        print(event)
        self.send_json(
            {
                'type': 'on.alarm',
                'content': event['content']
            }
        )

    def on_login(self, event):
        print('inside EventConsumer events_login()')
        print(event)
        self.send_json(
            {
                'type': 'on.login',
                'content': event['content']
            }
        )
