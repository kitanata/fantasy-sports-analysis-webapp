# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0019_auto_20160203_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='product',
            field=models.ForeignKey(related_name='product', to='subscriptions.Product', help_text='The product this subscription is for.'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(help_text='The user that owns this subscription.', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='uuid',
            field=models.CharField(db_index=True, max_length=128, editable=False, help_text='Recurly uuid.'),
        ),
    ]
