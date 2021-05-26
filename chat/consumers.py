import json
from user.models import UserProfile
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

@sync_to_async
def UpdateMessage(sender,receiver,message,time):
    messages=UserProfile.objects.get(username=receiver).Messages # get messages of user from database
    dict_messages=json.loads(messages) # convert to dictionary
    message_info={"message":message,"time":time} # dictionary with message information
    dict_messages.setdefault(sender,[]).append(message_info) # append the message to list in dictionary 
    json_messages=json.dumps(dict_messages) # convert dictionary to json
    UserProfile.objects.filter(username=receiver).update(Messages=json_messages) # update messages of user with new message in database

Connections={} # track online users

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # number of connections in a room
        if self.room_name in Connections.keys():
            Connections[self.room_name]+=1
        else:
            Connections[self.room_name]=1
        # accept the websocket connection
        await self.accept()
        # update client with receiver's online status
        await self.send(text_data=json.dumps(
        {
            'online': Connections[self.room_name]
        }))

    async def disconnect(self, close_code):
        # receiver went offline
        Connections[self.room_name]-=1
        # update sender with receiver's online status
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online',
                'online': Connections[self.room_name]
            }
        )
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']
        time = text_data_json['time']
        # Receiver is offline and Update message in database
        if receiver!="lobby" and Connections[self.room_name]<=1:
            await UpdateMessage(sender,receiver,message,time)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'time' : time
            }
        )
    # Receive message from room group for updating messages
    async def chat_message(self, event):
        message = event['message']
        time = event['time']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(
        {
            'message': message,
            'time' : time,
            'online': Connections[self.room_name]
        }))

    # Receive message from room group for updating online status
    async def online(self, event):
        online = event['online']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(
        {
            'online': online
        }))