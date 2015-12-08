# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0011_auto_20151201_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='recurly_plan_code',
            field=models.CharField(validators=[django.core.validators.RegexValidator(regex='(?i)[a-z0-9@\\-_\\.]')], unique=True, help_text='Used to uniquely identify the product in recurly.', verbose_name='Recurly Plan Code', blank=True, max_length=50),
        ),
    ]
