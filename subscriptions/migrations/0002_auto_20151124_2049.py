# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lineup',
            options={'get_latest_by': 'date_uploaded', 'verbose_name': 'Line Up'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='sport',
        ),
        migrations.AlterField(
            model_name='lineup',
            name='products',
            field=models.ManyToManyField(to='subscriptions.Product'),
        ),
    ]
