# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-28 16:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Committees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='UNKNOWN', max_length=32)),
                ('abbrevation', models.CharField(blank=True, default='', max_length=32)),
                ('begin_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommitteeTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='UNKNOWN', max_length=32)),
                ('abbrevation', models.CharField(blank=True, default='', max_length=32)),
                ('description', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='UNKNOWN', max_length=32)),
                ('abbrevation', models.CharField(blank=True, default='', max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DepartmentTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='UNKNOWN', max_length=32)),
                ('abbrevation', models.CharField(blank=True, default='', max_length=32)),
                ('description', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='UNKNOWN', max_length=32)),
                ('year', models.IntegerField(blank=True, max_length=4, null=True)),
                ('description', models.TextField(blank=True, default='')),
                ('begin_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('given_names', models.CharField(default='UNKNOWN', max_length=64)),
                ('preferred_name', models.CharField(default='UNKNOWN', max_length=32)),
                ('surname', models.CharField(default='UNKNOWN', max_length=32)),
                ('maiden_name', models.CharField(blank=True, default='', max_length=32)),
                ('nickname', models.CharField(blank=True, default='', max_length=32)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('student_id', models.CharField(blank=True, default='', max_length=10)),
                ('gender', models.CharField(choices=[('MA', 'Man'), ('WO', 'Woman'), ('UN', 'Unknown')], default='UN', max_length=2)),
                ('graduated', models.BooleanField(default=False)),
                ('graduated_year', models.IntegerField(blank=True, max_length=4, null=True)),
                ('dead', models.BooleanField(default=False)),
                ('mobile_phone', models.CharField(blank=True, default='', max_length=20)),
                ('phone', models.CharField(blank=True, default='', max_length=20)),
                ('street_address', models.CharField(blank=True, default='', max_length=64)),
                ('postal_code', models.CharField(blank=True, default='', max_length=64)),
                ('city', models.CharField(blank=True, default='', max_length=64)),
                ('country', django_countries.fields.CountryField(blank=True, default='', max_length=2)),
                ('url', models.CharField(blank=True, default='', max_length=64)),
                ('email', models.CharField(blank=True, default='', max_length=64)),
                ('subscribed_to_modulen', models.BooleanField(default=False)),
                ('allow_publish_info', models.BooleanField(default=True)),
                ('username', models.CharField(blank=True, default='', max_length=32)),
                ('crm_id', models.CharField(blank=True, default='', max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MembersCommitteesRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Committees')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Members')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MembersDepartmentsRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Departments')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Members')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MembersGroupsRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Groups')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Members')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MembersPostsRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Members')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='UNKNOWN', max_length=32)),
                ('members', models.ManyToManyField(through='members.MembersPostsRelation', to='members.Members')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PostTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='UNKNOWN', max_length=32)),
                ('description', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.AddField(
            model_name='posts',
            name='post_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.PostTypes'),
        ),
        migrations.AddField(
            model_name='memberspostsrelation',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Posts'),
        ),
        migrations.AddField(
            model_name='memberscommitteesrelation',
            name='post_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.PostTypes'),
        ),
        migrations.AddField(
            model_name='groups',
            name='members',
            field=models.ManyToManyField(through='members.MembersGroupsRelation', to='members.Members'),
        ),
        migrations.AddField(
            model_name='departments',
            name='members',
            field=models.ManyToManyField(through='members.MembersDepartmentsRelation', to='members.Members'),
        ),
        migrations.AddField(
            model_name='committees',
            name='committee_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.CommitteeTypes'),
        ),
        migrations.AddField(
            model_name='committees',
            name='members',
            field=models.ManyToManyField(through='members.MembersCommitteesRelation', to='members.Members'),
        ),
    ]