from django.urls import re_path
from .consumers import ReportConsumer  # Споживач, який ми створимо пізніше

websocket_urlpatterns = [
    re_path(r'ws/report/$', ReportConsumer.as_asgi()),  # Шлях до WebSocket
]