# Generated by Django 3.1.3 on 2021-07-28 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0004_patientvideos_whatsappmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='whatsappmessage',
            name='source_link',
        ),
    ]
