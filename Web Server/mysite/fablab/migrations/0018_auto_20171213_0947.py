# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-13 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fablab', '0017_auto_20171213_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardid',
            name='machine_user',
            field=models.ManyToManyField(to='fablab.Machine'),
        ),
    ]
