from channels.consumer import SyncConsumer
from asgiref.sync import async_to_sync
from bluetooth_interface import bt_functions
from time import sleep
from channels.layers import get_channel_layer
from control_system.consumers import CommandConsumer

class BackgroundTaskConsumer(SyncConsumer):
    """
    A consumer instance for managing Bluetooth devices.
    
    This consumer instance contains all of the necessary methods to
    interact with Bluetooth devices in the background. This enables
    channels to maintain connection with many consumer instances at
    the same time without blocking HTTP and WebSockets interaction.

    Attributes
    ----------
    self.device_group_name: dict
        A dict which holds a device id and channels group name as a key, value pair, respectively.
        This will enable this consumer object to send/receive device serial data to the corresponding WebSocket instance.

    self.sock: dict
        A dict which holds a device id , a BlueTooth socket instance and a port number as a key, value pair, respectively.
        example: { '14': <socket_instance> }

    Methods
    -------
    connect(message):
    listen(message):
    send_serial(message):
    disconnect(message):
    """

    def connect(self, message):
        # Remembers group name so that it has access to the current group and channels
        # TODO: Modify self.device_group_name so that it can hold multiple group names
        self.device_group_name = message['group_name']
        self.sock = {}

        # TODO: Assign port number dynamically
        self.port_num = 1

        sock, msg = bt_functions.connect(message['uuid'], self.port_num)
        if sock != 1: 
            # Hold sock instance in dict
            self.sock = {message['device']:[sock, self.port_num]}
            async_to_sync(self.channel_layer.group_send)(self.device_group_name,{'type': 'command_message', 'device':message['device'], 'message':msg })
        else:
            async_to_sync(self.channel_layer.group_send)(self.device_group_name,{'type': 'command_message', 'device':message['device'], 'message':msg })

    def listen(self, message):
        # TODO: Since only one background task would be running, loading many bluetooth devices will inevitably slow things down as they will be sharing the listening intervals.
        while(True):
            sleep(1)
            print('listen message here!')
            print(message)


    def send_serial(self, message):
        """Looks up device's id and sends message to it's sock instance"""
        id = int(message['device'])
        if id in self.sock.keys():
            print('sending message')
            result = bt_functions.send_serial(self.sock[id][0], message['message'])
            if result != 1:
                async_to_sync(self.channel_layer.group_send)(self.device_group_name,{'type': 'command_message', 'device':message['device'], 'message':result })
            else:
                async_to_sync(self.channel_layer.group_send)(self.device_group_name,{'type': 'command_message', 'device':message['device'], 'message':'Failed to send command' })


