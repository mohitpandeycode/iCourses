# Generated by Django 5.0.3 on 2024-03-16 09:40

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_remove_event_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=tinymce.models.HTMLField(blank=True),
        ),
    ]
