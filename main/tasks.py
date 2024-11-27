from asgiref.sync import async_to_sync
from celery import shared_task

from main.parseCore.parser import AsyncParser
from django.db import transaction
from sites.models import Site, SiteGoods
from django.db import connection

@shared_task
def task():
    sites = Site.objects.all()
    parser = AsyncParser(delay=.5)
    for site in sites:
        links = []
        for product in site.get_goods():
            links.append({'id': product.id, 'link': product.link})

        price_list = async_to_sync(parser.parse)(links, site.tags_trail)
        for price in price_list:
            try:
                with transaction.atomic():
                    product = SiteGoods.objects.get(pk=price['id'])
                    print(product.price_on_site)
                    product.set_price(price['price'])
                    product.save() 
                    print(product.price_on_site)


            except SiteGoods.DoesNotExist:
                print(f"Product with ID {price['id']} not found")
            
            finally:
                # Закрытие соединения после выполнения задачи
                connection.close()


