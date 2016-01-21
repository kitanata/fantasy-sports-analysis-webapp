# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0016_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='campaign_id',
            field=models.IntegerField(blank=True, help_text='ActiveCampaign Campaign to send on update.', null=True),
        ),
    ]
