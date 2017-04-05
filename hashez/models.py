# -*- coding: utf8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User as Person

states=(('OK','OK'),
        ('UPDATED','UPDATED'),
        ('FILESYSTEMERROR','FILESYSTEMERROR'),
        ('CRYPTOERROR','CRYPTOERROR'),
       )

class Client(models.Model):

  def __unicode__(self):
    return self.client

  client=models.CharField(max_length=128,unique=True)
  descr=models.TextField(blank=True)
  registred=models.DateTimeField(auto_now_add=True)

class FileSet(models.Model):

  def __unicode__(self):
    return u"{0}".format(self.id)

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

  types=((u'CHECK','Контроль'),
         ('UPDATE','Пересчёт'),
         ('NEWCLIENT','Новый клиент'),
         ('NEWFILESET','Новый набор файлов'),
        )

  results=(('PASS','Успешно'),
           ('FAIL','Неудачно')
          )

  def __unicode__(self):
    return unicode(self.eventType)

  eventType=models.CharField(max_length=32,choices=types)
  result=models.CharField(max_length=32,choices=results,blank=True,null=True)
  registred=models.DateTimeField(auto_now_add=True)
  client=models.ForeignKey(Client,null=True,blank=True)
  fileSet=models.ForeignKey(FileSet,null=True,blank=True)

class BadFiles(models.Model):

  def __unicode__(self):
    return self.path

  path=models.CharField(max_length=512)
  checksum=models.BinaryField(null=True)
  state=models.CharField(max_length=32,choices=states)
  event=models.ForeignKey(Event,null=True)

class Comment(models.Model):

  defaultTitle="""
                 
               """

  def __unicode__(self):
    return 0

  docNo=models.IntegerField()
  registred=models.DateTimeField(auto_now_add=True)
  title=models.TextField()
  reason=models.TextField()
  badFiles=models.ForeignKey(BadFiles,null=True)
  action=models.TextField()
  event=models.ForeignKey(Event,null=True)
  person=models.ForeignKey(Person,related_name='hashez_comment_person')
