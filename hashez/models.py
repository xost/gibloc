# -*- coding: utf8 -*-

from __future__ import unicode_literals

from django.db import models

class Client(models.Model):

  def __unicode__(self):
    return self.client

  client=models.CharField(max_length=128)
  descr=models.TextField(blank=True)
  registration=models.DateTimeField(auto_now_add=True)

class File(models.Model):

  states=(('OK','OK'),
          ('UPDATED','UPDATED'),
          ('FILESYSTEMERROR','FILESYSTEMERROR'),
          ('CRYPTOERROR','CRYPTOERROR'),
          ('NEW','NEW'),
          ('EMPTY','EMPTY'),
         )

  def __unicode__(self):
    return self.path
    
  path=models.CharField(max_length=512)
  checksum=models.BinaryField(null=True)
  state=models.CharField(max_length=32,choices=states)
  recalculate=models.DateTimeField(auto_now_add=False)
  client=models.ForeignKey(Client)

class Event(models.Model):

  states=(('CKECK','CHECK'),
          ('FAIL','FAIL'),
         )

  def __unicode__(self):
    return self.client

  client=models.ForeignKey(Client)
  eType=models.CharField(max_length=32,choices=states)
  lasttime=models.DateTimeField(auto_now_add=True)

class Diff(models.Model):

  def __unicode__(self):
    pass

  event=models.ForeignKey(Event)
  file=models.ForeignKey(File)
