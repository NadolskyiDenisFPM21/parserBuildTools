import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from main.routing import websocket_urlpatterns  # Імпортуємо маршрути


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parserBuildTools.settings')

# Якщо ви хочете використовувати тільки HTTP, залиште оригінальний код
# application = get_asgi_application()

# Для підтримки WebSocket змінюємо код на наступний:
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Оставляем поддержку HTTP
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  
            # Сюди ми додамо маршрути для WebSocket
        )
    ),
})