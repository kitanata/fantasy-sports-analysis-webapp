# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LineUp',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('pdf', models.FileField(upload_to='')),
                ('date_uploaded', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('duration', models.CharField(choices=[('daily', 'Daily'), ('monthly', 'Monthly')], max_length=24)),
                ('sport', models.CharField(max_length=24)),
                ('lineups', models.ManyToManyField(to='subscriptions.LineUp')),
            ],
        ),
    ]
