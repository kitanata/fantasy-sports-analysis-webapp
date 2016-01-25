# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('text', wagtail.wagtailcore.blocks.CharBlock()), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()))),
        ),
    ]
