# Generated by Django 3.1.3 on 2021-07-29 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0012_auto_20210728_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualsession',
            name='first_join',
            field=models.BooleanField(default=False, verbose_name='El usuario ha autorizado recibir mensajes por primera vez'),
        ),
    ]