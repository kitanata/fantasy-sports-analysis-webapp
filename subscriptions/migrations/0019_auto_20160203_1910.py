# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0018_auto_20160203_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sport',
            field=models.ForeignKey(null=True, help_text='Used to group together products.', on_delete=django.db.models.deletion.SET_NULL, to='subscriptions.Sport'),
        ),
    ]
