# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Provider, Client, SecurityQuestion, Login, Drop, Download

admin.site.register(Provider)
admin.site.register(Client)
admin.site.register(SecurityQuestion)
admin.site.register(Login)
admin.site.register(Drop)
admin.site.register(Download)
