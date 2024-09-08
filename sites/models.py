from django.db import models
from goods.models import Goods, Direction

class Site(models.Model):
    name = models.CharField(max_length=100, verbose_name='Сайт')
    link = models.URLField(max_length=500, verbose_name='Посилання')
    tags_trail = models.CharField(max_length=500, verbose_name='Шлях до контейнера', blank=True)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name='Напрямок', blank=True, null=True)

    def get_goods(self):
        return self.site_goods.all()

    def set_good_price(self, id, price):
        product = self.site_goods.get(pk=id)
        product.difference = price - product.goods.price
        product.price_on_site = price
        product.save()

    @property
    def difference_count(self):
        return self.site_goods.exclude(difference=0).count()

    @property
    def difference_percent(self):
        return int(round(self.difference_count/self.site_goods.count()*100))

    def __str__(self):
        return self.name


class SiteGoods(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='site_goods')
    link = models.URLField(max_length=500, verbose_name='Посилання на товар')
    price_on_site = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Ціна на сайті')
    difference = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Розбіжність')

    def __str__(self):
        return self.goods.name + ' ' + self.site.name
