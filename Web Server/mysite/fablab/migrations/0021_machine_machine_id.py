# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-08 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fablab', '0020_auto_20180108_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='machine_id',
            field=models.IntegerField(default=5),
        ),
    ]
