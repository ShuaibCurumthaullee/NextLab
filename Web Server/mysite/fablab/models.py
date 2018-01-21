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
    machine_id = models.CharField(max_length=100, null=False, default=5)
    machine_status = models.CharField(max_length=100, null=False, default="Available")

    def __str__(self):
        return self.machine_name

    class Meta:
        ordering = ('machine_name',)

class CardID(models.Model):
    cardID = models.CharField(max_length=200)
    machine_user = models.ForeignKey(Machine_User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.cardID

class Logs(models.Model):
	cardID = models.OneToOneField(CardID, on_delete=models.CASCADE)
	machine = models.OneToOneField(Machine, on_delete=models.CASCADE)
	start_time = models.DateTimeField(auto_now_add=True)
	finish_time = models.DateTimeField(null=True)
	duration = models.DateTimeField(null=True)
