# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-13 13:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20170309_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
                ('type', models.CharField(choices=[('PH', 'Phux'), ('OM', 'Ordinarie Medlem'), ('JS', 'JuniorStÄlM'), ('ST', 'StÄlM'), ('AA', 'Aktiv Alumn')], default='PH', max_length=2)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Member')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
