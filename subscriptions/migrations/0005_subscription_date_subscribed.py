# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0004_product_subscribed'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='date_subscribed',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
