# Generated by Django 4.2.5 on 2023-10-16 18:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0003_subscriptions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subscriptions',
            new_name='Subscriber',
        ),
    ]