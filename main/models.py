from django.db import models
from goods.models import Direction


class ParseReport(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва')
    file = models.FileField(upload_to='reports/', verbose_name='Файл')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name='Напрямок', blank=True, null=True)

    def __str__(self):
        return self.name
