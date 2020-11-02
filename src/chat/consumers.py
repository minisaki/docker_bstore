import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = 'chat_%s' % self.id
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat_mess',
                'message': message,
                'user_name': self.user.username,
                'user_url': self.user.profileuser.image.url,
                'datetime': now.isoformat(),
            }
        )

    def chat_mess(self, data):
        self.send(text_data=json.dumps(data))
