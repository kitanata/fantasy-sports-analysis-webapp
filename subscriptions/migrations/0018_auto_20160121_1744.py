# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0017_product_campaign_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='campaign_id',
        ),
        migrations.AddField(
            model_name='product',
            name='template_id',
            field=models.IntegerField(null=True, blank=True, help_text='ActiveCampaign template to use when sending updates.'),
        ),
    ]
