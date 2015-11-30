# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0005_subscription_date_subscribed'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineup',
            name='date_email_sent',
            field=models.DateTimeField(verbose_name='Last Email Sent', blank=True, null=True, help_text='Auto-filled. Records the last time an update email was sent to subscribers for this specific line up'),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', help_text="Displayed on a user's dashboard page, and in anymarketing messaging related to this product."),
        ),
        migrations.AlterField(
            model_name='lineup',
            name='date_uploaded',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='date_subscribed',
            field=models.DateField(default=django.utils.timezone.now, help_text='Records the date this subscription became active.'),
        ),
    ]
