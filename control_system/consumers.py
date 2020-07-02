# Dependencies 
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404, render
from datetime import datetime
import json

# Models
from .models import Device

# Error classes
from django.core.exceptions import ObjectDoesNotExist

#channel_layer = get_channel_layer()

class CommandConsumer(WebsocketConsumer):
    """ Channels consumer class for interfacing with websockets and the client."""

    def connect(self):
        """ """
        self.device_id = self.scope['url_route']['kwargs']['device_id']
        self.device_group_name = 'command_%s' % self.device_id
        device = Device.objects.get(id=self.device_id)

        # Connect to device by passing background-tasks info and group_name
        async_to_sync(self.channel_layer.send)('background-tasks', {
            'type': 'connect',
            'group_name': self.device_group_name,
            'uuid': device.uuid,
            'device' : device.id,
            }
        )

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.device_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.device_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        device_id = text_data_json['device']

        # Send message to device
        async_to_sync(self.channel_layer.send)('background-tasks', {
            'type': 'send_serial',
            'device': device_id,
            'message': message,
            }
        )

        # Send message to device group
        async_to_sync(self.channel_layer.group_send)(
            self.device_group_name,
            {
                'type': 'command_message',
                'message': message,
                'device': device_id
            }
        )

    def command_message(self, event):
        message = event['message']
        if type(message) != str:
            message = str(message)
        device_id = event['device']
        
        device = get_object_or_404(Device, id=device_id)
        history = device.get_command_history()
        now = datetime.now().strftime("%Y-%m-%d")
        if now in history:
            history[now] += (message + '\n')
        else:
            history[now] = (message + '\n')
        device.command_history = json.dumps(history)
        device.save()

        self.send(text_data=json.dumps({
            'message': device.command_history,
            'device': device_id
        }))
