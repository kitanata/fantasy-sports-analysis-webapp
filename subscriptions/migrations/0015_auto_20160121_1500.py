# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0014_auto_20151209_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='name',
            field=models.CharField(help_text='Will be used to group subscriptions together, should be a display friendly name', max_length=128),
        ),
    ]
