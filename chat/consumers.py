import json

from channels.generic.websocket import AsyncWebsocketConsumer
from articles.models import Team

connected_user = []
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        username = self.scope["user"].nickname
        if username in connected_user:
            pass
        else:
            print(connected_user)
            connected_user.append(username)
            print(connected_user)
            message = username + "님이 입장하셨습니다"
            await self.channel_layer.group_send(
                self.room_group_name, 
                {
                    "type": "chat_message", 
                    "message": message,
                    "username": "admin",
                    "connected_user": connected_user,
                }
            )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        username = self.scope["user"].nickname
        if username not in connected_user:
            pass
        else:
            connected_user.remove(username)
            message = username + "님이 퇴장하셨습니다"
            await self.channel_layer.group_send(
                self.room_group_name, 
                {
                    "type": "chat_message", 
                    "message": message,
                    "username": "admin",
                    "connected_user": connected_user,
                }
            )


    # Receive message from WebSocket
    async def receive(self, text_data):
        username = self.scope["user"].nickname
        userPk = self.scope["user"].pk
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
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
        username = event["username"]
        # connected_user = event["connected_user"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "username": username, "connected_user": connected_user,}))