# -*- coding: utf8 -*-

from __future__ import unicode_literals

from django.db import models

states=(('OK','OK'),
        ('UPDATED','UPDATED'),
        ('FILESYSTEMERROR','FILESYSTEMERROR'),
        ('CRYPTOERROR','CRYPTOERROR'),
        ('NEW','NEW'),
        ('EMPTY','EMPTY'),
       )

class Client(models.Model):

  def __unicode__(self):
    return self.client

  client=models.CharField(max_length=128,unique=True)
  descr=models.TextField(blank=True)
  registred=models.DateTimeField(auto_now_add=True)

class FileSet(models.Model):

  def __unicode__(self):
    return self.id

  registred=models.DataTimeField(auto_now_add=True)

class File(models.Model):

  def __unicode__(self):
    return self.path
    
  path=models.CharField(max_length=255)
  checksum=models.BinaryField(null=True)
  state=models.CharField(max_length=32,choices=states)
  updated=models.DateTimeField(auto_now_add=False)
  fsCount=models.ForeignKey(FileSet)
  client=models.ForeignKey(Client)

  class Meta():
    unique_together=('path','fsCount','id')

class Event(models.Model):

  types=(('CKECK','CHECK'),
         ('UPDATE','UPDATE'),
         ('NEWCLIENT','NEWCLIENT'),
         ('NEWFILESET','NEWFILESET'),
        )

  def __unicode__(self):
    return self.client

  client=models.ForeignKey(Client)
  eventType=models.CharField(max_length=32,choices=types)
  happened=models.DateTimeField(auto_now_add=True)

class Diff(models.Model):

  def __unicode__(self):
    pass

  event=models.ForeignKey(Event)
  path=models.CharField(max_length=512)
  state=models.CharField(max_length=32,choices=states)
