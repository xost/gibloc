# -*- coding: utf-8 -*-

from django.db import models,IntegrityError

class Site(models.Model):
  item=models.CharField(max_length=20,primary_key=True)
  descr=models.CharField(max_length=100,blank=True)
  m2mf=['']
  prelink='http://'
  postlink=''

  def __unicode__(self):
    return '%s' % self.item

class SiteACLs(models.Model):
  item=models.CharField(max_length=10,primary_key=True)
  descr=models.CharField(max_length=100,blank=True)
  Site=models.ManyToManyField(Site,blank=True)
  m2mf=['/Site']
  prelink=''
  postlink=''

  def __unicode__(self):
    return '%s' % self.item

class Host(models.Model):
  item=models.CharField(max_length=20,primary_key=True)
  descr=models.CharField(max_length=100,blank=True)
  m2mf=['']
  prelink='http://'
  postlink='.gib.loc'

  def __unicode__(self):
    return self.item

class HostACLs(models.Model):
  item=models.CharField(max_length=10,primary_key=True)
  descr=models.CharField(max_length=100,blank=True)
  Host=models.ManyToManyField(Host,blank=True)
  SiteACLs_deny=models.ManyToManyField(SiteACLs,related_name='siteacls_deny',blank=True)
  SiteACLs_allow=models.ManyToManyField(SiteACLs,related_name='siteacls_allow',blank=True)
  m2mf=['/Host','/SiteACLs_deny','/SiteACLs_allow']
  prelink=''
  postlink=''

  def __unicode__(self):
    return self.item
