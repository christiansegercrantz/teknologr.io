# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-28 17:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20160428_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='graduated_year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
