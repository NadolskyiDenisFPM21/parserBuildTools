from django.db import models


class Direction(models.Model):
    name = models.CharField(max_length=100, verbose_name='Напрямок')

    def __str__(self):
        return self.name


class Goods(models.Model):
    sku = models.CharField(max_length=10, verbose_name="SKU")
    name = models.CharField(max_length=200, verbose_name="Назва")
    price = models.DecimalField(decimal_places=2, verbose_name="Ціна", max_digits=15)
    directions = models.ManyToManyField(Direction, related_name="goods", verbose_name="Напрямки",
                                        blank=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = verbose_name + "и"
        ordering = ['sku']

    def __str__(self):
        return self.name + " " + self.sku
