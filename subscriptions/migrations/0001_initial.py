# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LineUp',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to='')),
                ('date_uploaded', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Line Up',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('duration', models.CharField(max_length=24, choices=[('daily', 'Daily'), ('monthly', 'Monthly')])),
                ('sport', models.CharField(max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(to='subscriptions.Product')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='lineup',
            name='products',
            field=models.ManyToManyField(to='subscriptions.Product', blank=True),
        ),
    ]
