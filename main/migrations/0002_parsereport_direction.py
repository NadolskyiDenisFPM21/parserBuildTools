# Generated by Django 4.2.15 on 2024-08-28 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_direction_goods_directions'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parsereport',
            name='direction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.direction', verbose_name='Напрямок'),
        ),
    ]
