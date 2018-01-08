# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Machine_User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
    

class Machine(models.Model):
    machine_name = models.CharField(max_length=100)
    machine_user = models.ManyToManyField(Machine_User)

    def __str__(self):
        return self.machine_name

    class Meta:
        ordering = ('machine_name',)

class CardID(models.Model):
    cardID = models.CharField(max_length=200)
    machine_user = models.OneToOneField(Machine_User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.cardID
