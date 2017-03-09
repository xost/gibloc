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

  registred=models.DateTimeField(auto_now_add=True)
  client=models.ForeignKey(Client)

class File(models.Model):

  def __unicode__(self):
    return self.path
    
  path=models.CharField(max_length=255)
  checksum=models.BinaryField(null=True)
  state=models.CharField(max_length=32,choices=states)
  updated=models.DateTimeField(auto_now_add=False)
  fileSet=models.ForeignKey(FileSet)

  class Meta():
    unique_together=('path','fileSet')

class Event(models.Model):

  types=(('CKECK','CHECK'),
         ('UPDATE','UPDATE'),
         ('NEWCLIENT','NEWCLIENT'),
         ('NEWFILESET','NEWFILESET'),
        )

  results=(('PASS','PASS'),
           ('FAIL','FAIL')
          )

  def __unicode__(self):
    return unicode(self.eventType)

  eventType=models.CharField(max_length=32,choices=types)
  comment=models.CharField(max_length=255,blank=True,null=True)
  registred=models.DateTimeField(auto_now_add=True)
  client=models.ForeignKey(Client)

class Diff(models.Model):

  def __unicode__(self):
    return self.path

  path=models.CharField(max_length=512)
  state=models.CharField(max_length=32,choices=states)
  event=models.ForeignKey(Event)
  fileSet=models.ForeignKey(FileSet)
