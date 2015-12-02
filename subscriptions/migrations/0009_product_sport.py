# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0008_auto_20151201_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sport',
            field=models.ForeignKey(to='subscriptions.Sport', null=True),
        ),
    ]
