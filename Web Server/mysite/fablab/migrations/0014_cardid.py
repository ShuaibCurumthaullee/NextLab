# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-12 14:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fablab', '0013_remove_machine_user_user_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='cardID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardID', models.CharField(max_length=200)),
                ('machine_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fablab.Machine_User')),
            ],
        ),
    ]
