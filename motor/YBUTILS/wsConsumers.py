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

class JSONConsumer(JsonWebsocketConsumer):

    def connect(self):
        # print("_________________________")
        # print(self.scope["user"])
        # print(self.scope["token"])
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name

        # # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # async_to_sync(self.channel_layer.group_add)(
        #     "events",
        #     self.channel_name
        # )

        self.accept()
        # async_to_sync(self.channel_layer.send)(self.channel_name, {"type": "on.login", "content": "correcto"})
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "on.login",
                "content": "correcto",
            }
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'events',
            self.channel_name
        )
        self.close()

    def envia(channel, grupo, mensaje):
        async_to_sync(channel.group_send)(
            "events",
            {
                "type": "send.msg",
                "content": "enviamosdesdeapi",
            }
        )

    def receive_json(self, content, **kwargs):
        # self.send_json(content)
        # TODO groupSend, channelSend, api
        if content["type"] == "legacy":
            prefix = content["prefix"]
            pk = content["pk"] if "pk" in content else "--static--"
            params = content["params"] if "params" in content else {"params": None}
            action = content["action"] if "action" in content else None
            try:
                obj = qsa.from_project("formAPI").entry_point("websocket", prefix, pk, params, action)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        "type": "send.msg",
                        "content": obj,
                    }
                )
            except Exception as e:
                print(e)
                self.send_json({"error": content})
        elif content["type"] == "channelSend":
            try:
                obj = qsa.from_project("formAPI").entry_point("websocket", prefix, pk, params, action)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        "type": "send.msg",
                        "content": obj,
                    }
                )
            except Exception as e:
                print(e)
                self.send_json({"error": content})
        elif content["type"] == "groupSend":
            try:
                obj = qsa.from_project("formAPI").entry_point("websocket", prefix, pk, params, action)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        "type": "send.msg",
                        "content": obj,
                    }
                )
            except Exception as e:
                print(e)
                self.send_json({"error": content})
        # prifnt(content)

    def send_msg(self, event):
        # TODO posibilidad de poner un from quien envio?
        self.send_json(
            {
                'type': 'send.msg',
                'content': event['content']
            }
        )

    def on_login(self, event):
        # TODO enviar al grupo quien conecto
        self.send_json(
            {
                'type': 'on.login',
                'content': event['content']
            }
        )
