# Generated by Django 5.0.4 on 2024-05-19 18:07

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_children'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Children',
            new_name='Child',
        ),
    ]
