# Generated by Django 3.2.9 on 2021-11-12 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0009_user_no_session_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='no_session_message',
        ),
        migrations.AddField(
            model_name='user',
            name='last_time_block',
            field=models.DateTimeField(null=True, verbose_name='Ultima fecha en la que el usuario fue bloqueado'),
        ),
        migrations.AddField(
            model_name='user',
            name='no_session_message_count',
            field=models.IntegerField(default=False, verbose_name='Cuenta la cantidad de mensajes que se responde al usuario'),
        ),
    ]
