# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_auto_20151123_1815'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lineup',
            options={'verbose_name': 'Line Up'},
        ),
    ]
