# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_auto_20151123_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='lineups',
        ),
        migrations.AddField(
            model_name='lineup',
            name='subscriptions',
            field=models.ManyToManyField(to='subscriptions.Subscription', blank=True),
        ),
    ]
