# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-02 08:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fablab', '0006_delete_bigmachines'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Machines',
            new_name='Machine',
        ),
    ]
