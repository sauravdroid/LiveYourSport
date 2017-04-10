# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-08 08:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedCSV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=64, unique=True)),
                ('csv_file', models.FileField(upload_to=b'')),
            ],
        ),
    ]
