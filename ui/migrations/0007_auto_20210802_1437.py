# Generated by Django 3.1.3 on 2021-08-02 19:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0006_auto_20210802_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='authorization_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Tiempo en que el usuario autoriza recibir mensajes'),
        ),
    ]
