# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-08-16 16:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_auto_20170502_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='allow_publish_info',
            field=models.BooleanField(default=False),
        ),
    ]
