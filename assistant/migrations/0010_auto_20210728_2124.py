# Generated by Django 3.1.3 on 2021-07-28 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0009_virtualsession_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virtualsession',
            name='start_time',
            field=models.DateTimeField(verbose_name='Tiempo de Inicio'),
        ),
    ]
