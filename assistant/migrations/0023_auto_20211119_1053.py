# Generated by Django 3.2.9 on 2021-11-19 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0022_virtualsession_is_session_expired'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualsession',
            name='user_presession_notified',
            field=models.BooleanField(default=False, verbose_name='Notificación al usuario 12 horas antes de la sesión'),
        ),
        migrations.AlterField(
            model_name='virtualsession',
            name='user_authorized',
            field=models.BooleanField(default=False, verbose_name='El usuario confirma la sesión'),
        ),
    ]
