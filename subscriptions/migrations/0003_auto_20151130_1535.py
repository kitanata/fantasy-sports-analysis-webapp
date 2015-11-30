# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_auto_20151124_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineup',
            name='date_uploaded',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
