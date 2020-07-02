from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'(?P<device_id>\w+)/ws/console/$', consumers.CommandConsumer),
]
