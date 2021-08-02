# Generated by Django 3.1.3 on 2021-08-02 19:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0005_auto_20210730_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='authorization_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Tiempo en que el usuario autoriza recibir mensajes'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='first_join',
            field=models.BooleanField(default=True, verbose_name='El usuario ha autorizado recibir mensajes'),
        ),
    ]
