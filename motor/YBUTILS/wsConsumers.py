from channels.generic.websocket import JsonWebsocketConsumer
import json
from asgiref.sync import async_to_sync

class MyConsumer(JsonWebsocketConsumer):

  def connect(self):
    print('inside EventConsumer connect()')
    async_to_sync(self.channel_layer.group_add)(
        'events',
        self.channel_name
    )
    self.accept()
    async_to_sync(self.channel_layer.group_send)(
        "events",
        {
            "type": "events.alarm",
            "text": "test",
         },
    )

  def disconnect(self, close_code):
    print('inside EventConsumer disconnect()')
    print("Closed websocket with code: ", close_code)
    async_to_sync(self.channel_layer.group_discard)(
        'events',
        self.channel_name
    )
    self.close()

  def receive_json(self, content, **kwargs):
    print('inside EventConsumer receive_json()')
    print("Received event: {}".format(content))
    self.send_json(content)

  def events_alarm(self, event):
    print('inside EventConsumer events_alarm()')
    self.send_json(
        {
            'type': 'events.alarm',
            'content': "event['content']"
        }
    )

#https://github.com/andrewgodwin/channels-examples/blob/master/multichat/chat/utils.py
