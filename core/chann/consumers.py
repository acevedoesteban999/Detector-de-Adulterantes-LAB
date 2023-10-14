import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


consumers=[]
def send_message(message):
    global consumers
    for c in consumers:
        c.send(message)

class Consumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        global consumers
        self._consumer_index=len(consumers)
        consumers.append(self)
    def _send(self,message):
        self.send(text_data=message)
    def disconnect(self, close_code):
        global consumers
        del consumers[self._consumer_index]