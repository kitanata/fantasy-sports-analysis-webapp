# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0022_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineup',
            name='template_id',
            field=models.IntegerField(null=True, help_text='ActiveCampaign template to use when sending updates.', blank=True),
        ),
    ]
