# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0014_auto_20151209_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='list_id',
            field=models.IntegerField(help_text='ActiveCampaign mailing list ID.', blank=True, null=True),
        ),
    ]
