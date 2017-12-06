# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Machine_User
from .models import Machine

admin.site.register(Machine_User)
admin.site.register(Machine)
