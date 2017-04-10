# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-08 07:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=64, unique=True)),
                ('order_status', models.CharField(max_length=64)),
                ('product_code', models.CharField(max_length=64)),
                ('product_name', models.TextField()),
                ('product_url', models.TextField()),
                ('cost_price', models.TextField()),
            ],
        ),
    ]
