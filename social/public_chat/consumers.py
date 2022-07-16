import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    # when user enters a new room
    async def connect(self):
        # get room name
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # get group name
        self.room_group_name = 'chat_%s' % self.room_name
        # connect to websocket
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    # when user disconnects from a room
    async def disconnect(self, close_code):
        # discard room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    # when user sends a message
    async def receive(self, text_data):
        # load json data
        text_data_json = json.loads(text_data)
        # get message
        message = text_data_json['message']
        # send the message to chat_message event  
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'chat_message',
                'message' : message
            }
        )
    # when user sends a message
    async def chat_message(self, event):
        # get message
        message = event['message']
        # send message
        await self.send(text_data=json.dumps({
            'message' : message
        }))