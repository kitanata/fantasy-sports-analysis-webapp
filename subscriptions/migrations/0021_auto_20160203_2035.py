# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0020_auto_20160203_2013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lineup',
            old_name='uploaded_pdf',
            new_name='pdf',
        ),
    ]
