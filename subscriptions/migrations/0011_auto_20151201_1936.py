# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0010_auto_20151201_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='date_subscribed',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Subscribed', help_text='Records the date this subscription became active.'),
        ),
    ]
