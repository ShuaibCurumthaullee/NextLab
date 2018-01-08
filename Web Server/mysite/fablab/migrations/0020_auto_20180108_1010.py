# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-08 09:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fablab', '0019_auto_20171213_0957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardid',
            name='machine',
        ),
        migrations.RemoveField(
            model_name='cardid',
            name='machine_user',
        ),
        migrations.AddField(
            model_name='cardid',
            name='machine_user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='fablab.Machine_User'),
        ),
    ]