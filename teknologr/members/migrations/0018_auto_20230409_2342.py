# Generated by Django 3.1.14 on 2023-04-09 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0017_member_allow_studentbladet'),
    ]

    operations = [
        migrations.AddField(
            model_name='decoration',
            name='comment',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='functionarytype',
            name='comment',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='grouptype',
            name='comment',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='decorationownership',
            name='decoration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ownerships', to='members.decoration'),
        ),
        migrations.AlterField(
            model_name='functionary',
            name='functionarytype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='functionaries', to='members.functionarytype'),
        ),
        migrations.AlterField(
            model_name='group',
            name='grouptype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='members.grouptype'),
        ),
        migrations.AlterField(
            model_name='groupmembership',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='members.group'),
        ),
    ]