# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-10 08:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_scrapedcsv'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrapedcsv',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 10, 8, 30, 47, 222759, tzinfo=utc)),
        ),
    ]
