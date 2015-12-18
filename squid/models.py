from django.db import models
import socket

class HostManager(models.Manager):
  def all(self,**kwargs):
    objects=super(HostManager,self).all(**kwargs)
    for obj in objects:
      try:
        obj.alt=socket.gethostbyname('%s.gib.loc' % obj.item)
      except socket.gaierror,e:
        obj.error='Socket error: ' % e
    return objects

class Host(models.Model):
  item=models.CharField(max_length=20,primary_key=True)
  descr=models.CharField(max_length=100,blank=True)
  objects=HostManager()

  def __unicode__(self):
    return '%s'%self.item

class HostACLs(models.Model):
  name=models.CharField(max_length=10,primary_key=True)
  descr=models.CharField(max_length=100,blank=True)
  items=models.ManyToManyField(Host,blank=True)

  def __unicode__(self):
    return '%s'%self.name

class Port(models.Model):
  item=models.DecimalField(max_digits=5,decimal_places=0,primary_key=True)
  descr=models.CharField(max_length=100,blank=True)

  def __unicode__(self):
    return '%s'%self.item

class PortACLs(models.Model):
  name=models.CharField(max_length=10,primary_key=True)
  descr=models.CharField(max_length=100,blank=True)
  items=models.ManyToManyField(Port,blank=True)

  def __unicode__(self):
    return '%s'%self.name

class Url(models.Model):
  item=models.URLField(max_length=20,primary_key=True)
  descr=models.CharField(max_length=100,blank=True)

  def __unicode__(self):
    return '%s'%str(self.item)

class UrlACLs(models.Model):
  name=models.CharField(max_length=10,primary_key=True)
  descr=models.CharField(max_length=100,blank=True)
  items=models.ManyToManyField(Url,blank=True)

  def __unicode__(self):
    return '%s'%self.name

