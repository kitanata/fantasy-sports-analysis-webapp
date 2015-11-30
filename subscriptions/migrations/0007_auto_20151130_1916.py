# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0006_auto_20151130_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineup',
            name='date_uploaded',
            field=models.DateTimeField(verbose_name='Date Uploaded', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='date_subscribed',
            field=models.DateField(help_text='Records the date this subscription became active.', verbose_name='Date Subscribed', default=django.utils.timezone.now),
        ),
    ]
