from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
import control_system.routing
from bluetooth_interface.consumers import BackgroundTaskConsumer

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            control_system.routing.websocket_urlpatterns
        )
    ),
    'channel': ChannelNameRouter({
        'background-tasks': BackgroundTaskConsumer,
    })
})
