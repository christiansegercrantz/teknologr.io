# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-13 15:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_membertype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='stalm',
        ),
    ]
