import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ReportConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'report_group'  # Група для повідомлень

        # Приєднуємося до групи
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Відключаємося від групи
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Отримуємо повідомлення від WebSocket
    async def receive(self, text_data):

        # Відправляємо повідомлення в групу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'report_message',
                'status': True,
            }
        )

    # Отримуємо повідомлення від групи
    async def report_message(self, event):
        message = event['message']

        # Відправляємо повідомлення WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
