# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0010_change_on_delete_behaviour'),
        ('subscriptions', '0017_auto_20160203_1819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AddField(
            model_name='product',
            name='marketing_image',
            field=models.ForeignKey(blank=True, null=True, related_name='+', to='wagtailimages.Image', help_text="Displayed on a user's dashboard page, and in anymarketing messaging related to this product.", on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
