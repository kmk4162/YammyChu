import json

from channels.generic.websocket import AsyncWebsocketConsumer
from articles.models import Team

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        username = self.scope["user"].nickname
        userPk = self.scope["user"].pk
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        print(userPk)
        message = username + ":" +  message + ":" + str(userPk)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                "type": "chat_message", 
                "message": message,
                "username": username,
            }
        )
    async def chat_message(self, event):
        message = event["message"]
        username = self.scope["user"].nickname
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "username": username, "test": "test",}))