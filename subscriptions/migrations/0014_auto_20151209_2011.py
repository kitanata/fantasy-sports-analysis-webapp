# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0013_auto_20151204_2026'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='date_subscribed',
            new_name='activated_at',
        ),
        migrations.AddField(
            model_name='subscription',
            name='canceled_at',
            field=models.DateTimeField(null=True, verbose_name='Date Cancelled', blank=True, help_text='Records the date this subscription was cancelled.'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='expired_at',
            field=models.DateTimeField(null=True, verbose_name='Date Expired', blank=True, help_text='Records the date this subscription expired, or will expire.'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='state',
            field=models.CharField(max_length=64, choices=[('active', 'active'), ('canceled', 'canceled'), ('future', 'future'), ('expired', 'expired')], default='expired'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='uuid',
            field=models.CharField(max_length=128, default='a', db_index=True),
            preserve_default=False,
        ),
    ]
