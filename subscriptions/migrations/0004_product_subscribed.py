# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscriptions', '0003_auto_20151130_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subscribed',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='subscriptions.Subscription'),
        ),
    ]
