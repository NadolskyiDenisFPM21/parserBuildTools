from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from main.parseCore.parser import AsyncParser
from django.db import transaction
from sites.models import Site, SiteGoods
from django.db import connection

@shared_task
def task():
    sites = Site.objects.all()
    # sites = Site.objects.filter(id=15)
    parser = AsyncParser(delay=.5)

    # Получаем канал для отправки сообщений через WebSocket
    channel_layer = get_channel_layer()

    for site in sites:
        print(f"Start parsing {site.name}")
        links = []
        for product in site.get_goods():
            links.append({'id': product.id, 'link': product.link})

        price_list = async_to_sync(parser.parse)(links, site.tags_trail)

        for price in price_list:
            try:
                with transaction.atomic():
                    product = SiteGoods.objects.get(pk=price['id'])
                    product.set_price(price['price'])
                    product.save() 

            except SiteGoods.DoesNotExist:
                print(f"Product with ID {price['id']} not found")
            
            finally:
                # Закрытие соединения после выполнения задачи
                connection.close()

    # Отправка сообщения по завершению задачи
    async_to_sync(channel_layer.group_send)(
        'report_group',  # Группа, которая будет слушать этот канал
        {
            'type': 'report_message',  # Тип сообщения (в нашем случае это пользовательский тип)
            'message': 'Task completed successfully, new prices have been updated'  # Сообщение
        }
    )
