# Generated by Django 4.2.15 on 2024-08-08 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParseReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Назва')),
                ('file', models.FileField(upload_to='reports/', verbose_name='Файл')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Створено')),
            ],
        ),
    ]
