from asgiref.sync import async_to_sync
from celery import shared_task

from main.parseCore.parser import AsyncParser

from sites.models import Site


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
            site.set_good_price(price['id'], price['price'])

    return "Task Complete"

