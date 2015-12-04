# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0012_product_recurly_plan_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='duration',
            field=models.CharField(help_text='Choose whether this product is a monthly subscription or a one day purchase.', max_length=24, choices=[('days', 'Daily'), ('months', 'Monthly')]),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(default=Decimal('0.00'), help_text='Price of the product', max_digits=8, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='product',
            name='recurly_plan_code',
            field=models.CharField(validators=[django.core.validators.RegexValidator(regex='(?i)[a-z0-9@\\-_\\.]', message='Code entered must only contain alphanumeric characters, as well as @, -, _, and .')], help_text='Used to uniquely identify the product in recurly.', unique=True, verbose_name='Recurly Plan Code', max_length=50),
        ),
    ]
