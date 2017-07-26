# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
import random
import humanize
import string
from datetime import datetime
import pytz

def randstring(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

class Provider(models.Model):
    name = models.CharField(max_length=128)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name

class Client(models.Model):
    provider = models.ForeignKey(Provider)
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=12, unique=True, default=randstring(8))
    session_time = models.IntegerField(default=3600)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name

class SecurityQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=256)
    answer = models.CharField(max_length=256)
    hint = models.CharField(max_length=256)
    client = models.ForeignKey(Client)
    lowercase = models.BooleanField(default=False)

    def name(self):
        return str(self.id)[:6]

    def verify(self, string):
        answer = self.answer
        if self.lowercase:
            string = string.lower()
            answer = answer.lower()
        return string == answer

    def __str__(self):
        return self.question[:32]

class Login(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client)
    successful = models.BooleanField()
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        success = "unknown status"
        if self.successful:
            success = "successful"
        else:
            success = "unsuccessful"
        return "(" + str(humanize.naturaltime(datetime.now(pytz.UTC) - self.time)) + ", " + success + ") attempted login to " + self.client.name + " (" + str(self.client.id) + ")"

class Drop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    modified_date = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    data_type = models.CharField(max_length=32)
    client = models.ForeignKey(Client)
    downloads = models.IntegerField(default=0)
    max_downloads = models.IntegerField(default=None, null=True, blank=True)
    file = models.FileField(upload_to="uploads/clients/" + str(uuid.uuid4())) # random UUID for data compartmentalization and separation

    def expires(self):
        if not self.expiration_date:
            return "never"
        return str(humanize.naturaltime(datetime.now(pytz.UTC) - self.expiration_date))

    def technical_name(self):
        return str(self.id)[:12]

    def created(self):
        return str(humanize.naturaltime(datetime.now(pytz.UTC) - self.modified_date))

    def max_downloads_hr(self):
        if self.max_downloads:
            return "/" + str(self.max_downloads)
        return ""

    def is_expired(self):
        if self.max_downloads:
            if self.downloads >= self.max_downloads:
                return True
        if self.expiration_date == None:
            return False
        if self.expiration_date > datetime.now(pytz.UTC):
            return False
        return True

    def __str__(self):
        return self.name

class Download(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client)
    successful = models.BooleanField()
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    time = models.DateTimeField(auto_now=True)
    drop = models.ForeignKey(Drop)

    def __str__(self):
        return "(" + str(humanize.naturaltime(datetime.now(pytz.UTC) - self.time)) + ") " + self.client.name + " downloaded drop '" + str(self.drop.name) + "'"
