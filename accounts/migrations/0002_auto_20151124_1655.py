# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailuser',
            name='first_name',
            field=models.CharField(verbose_name='first name', blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='emailuser',
            name='last_name',
            field=models.CharField(verbose_name='last name', blank=True, max_length=255),
        ),
    ]
