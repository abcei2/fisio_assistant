# Generated by Django 3.1.3 on 2021-07-28 16:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.TextField(max_length=1024, verbose_name='Titulo')),
                ('source_link', models.TextField(max_length=1024, verbose_name='Titulo')),
                ('description', models.TextField(blank=True, max_length=4096, verbose_name='Descripción')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
