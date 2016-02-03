# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0004_capitalizeverbose'),
        ('subscriptions', '0015_auto_20160121_1500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineup',
            name='pdf',
        ),
        migrations.AddField(
            model_name='lineup',
            name='uploaded_pdf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='wagtaildocs.Document', blank=True, related_name='+', null=True),
        ),
    ]
