# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-11 19:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fablab', '0011_machine_user_card_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='machine_user',
            old_name='card_id',
            new_name='user_code',
        ),
    ]
