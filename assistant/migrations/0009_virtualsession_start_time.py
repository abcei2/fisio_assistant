# Generated by Django 3.1.3 on 2021-07-28 21:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0008_auto_20210728_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualsession',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Tiempo de Inicio'),
            preserve_default=False,
        ),
    ]
