# -*- coding: utf-8 -*-

from django.core.validators import RegexValidator
from django.db import models

alphanumeric=RegexValidator(r'^[\-0-9a-zA-Zа-яА-Я\"\']*$','Only alphanumeric characters are allowed')

class OwnerG(models.Model):
  item=models.CharField(max_length=20,unique=True,validators=[alphanumeric])
  descr=models.CharField(max_length=100,blank=True)
  member='Owner'

  def __unicode__(self):
    return self.item

class Owner(models.Model):
  item=models.CharField(max_length=100)
  descr=models.CharField(max_length=100,blank=True)
  registration=models.DateTimeField(auto_now_add=True)
  group=models.ForeignKey(OwnerG)

  def __unicode__(self):
    return self.item

class LicenseG(models.Model):
  item=models.CharField(max_length=20,unique=True,validators=[alphanumeric])
  descr=models.CharField(max_length=20,blank=True)
  member='License'

  def __unicode__(self):
    return self.item

class License(models.Model):
  item=models.CharField(max_length=50,blank=False,null=False,validators=[alphanumeric])
  descr=models.CharField(max_length=100,blank=True)
  registration=models.DateTimeField(auto_now_add=True)
  changestate=models.DateTimeField(auto_now=True)
  owner=models.ForeignKey(Owner,null=True,blank=True,on_delete=models.SET_NULL)
  group=models.ForeignKey(LicenseG)

  def __unicode__(self):
    return self.item
