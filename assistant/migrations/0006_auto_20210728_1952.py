# Generated by Django 3.1.3 on 2021-07-28 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0005_remove_whatsappmessage_source_link'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PatientVideos',
            new_name='WhatsAppMessageVideos',
        ),
    ]