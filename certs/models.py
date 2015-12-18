# -*- coding: utf8 -*-

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
import actions,repeat

class Issuer(models.Model):
  #item=models.CharField(unique=True,max_length=100,verbose_name=u'Издатель')
  item=models.CharField(unique=False,max_length=100,verbose_name=u'Издатель')
  descr=models.TextField(blank=True,verbose_name=u'Описание')
  registration=models.DateTimeField(auto_now_add=True)
  contact=models.TextField(blank=True,verbose_name=u'Контакты')

  def __unicode__(self):
    return self.item

  class Meta:
    verbose_name=u'Издатель'
    verbose_name_plural=u'Издатели'

class Owner(models.Model):
  item=models.CharField(unique=True,max_length=50,verbose_name=u'Сотрудник')
  descr=models.CharField(max_length=100,blank=True,verbose_name='Описание')
  email=models.CharField(max_length=200,blank=True,verbose_name=u'E-MAIL')
  registration=models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return self.item

  class Meta:
    verbose_name=u'Сотрудник'
    verbose_name_plural=u'Сотрудники'

class Skzi(models.Model):
  item=models.CharField(unique=True,max_length=50,verbose_name=u'СКЗИ')
  descr=models.CharField(max_length=100,blank=True,verbose_name=u'Описание')
  registration=models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return self.item

  class Meta:
    verbose_name=u'СКЗИ'
    verbose_name_plural=u'СКЗИ'

class Area(models.Model):
  item=models.CharField(unique=True,max_length=255,verbose_name=u'Область действия')
  descr=models.CharField(max_length=100,blank=True,verbose_name=u'Описание')
  registration=models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return self.item

  class Meta:
    verbose_name=u'Область действия'
    verbose_name_plural=u'Области действия'

class Type(models.Model):
  item=models.CharField(unique=True,max_length=100,verbose_name=u'Вид ключевой информации')
  descr=models.CharField(max_length=100,blank=True,verbose_name=u'Описание')
  registration=models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return self.item

  class Meta:
    verbose_name=u'Вид ключевой информации'
    verbose_name_plural=u'Виды ключевой информации'

class Group(models.Model):
  item=models.CharField(max_length=50,unique=True,verbose_name=u'Группа сертификатов')
  descr=models.CharField(max_length=100,blank=True,verbose_name=u'Описание')
  registration=models.DateTimeField(auto_now_add=True)
  cheif=models.ForeignKey(Owner,verbose_name=u'Ответственный')
  email=models.CharField(max_length=200,blank=True,verbose_name=u'E-MAIL')

  def __unicode__(self):
    return self.item

  class Meta:
    verbose_name=u'Группа сертификатов'
    verbose_name_plural=u'Группы сертификатов'

class Cert(models.Model):
  item=models.CharField(max_length=100,unique=True,verbose_name=u'Серийный номер')
  descr=models.TextField(blank=True,verbose_name=u'Описание')
  registration=models.DateTimeField(auto_now_add=True)
  starttime=models.DateField(verbose_name=u'Начало действия')
  deadtime=models.DateField(verbose_name=u'Конец действия')
  repeat=models.IntegerField(choices=repeat.repeat.as_list(),blank=True,null=True,verbose_name=u'Выполнять')
  nday=models.IntegerField(blank=True,null=True,verbose_name=u'День')
  action=models.IntegerField(choices=actions.actions.as_list(),blank=True,null=True,verbose_name=u'Действие')
  email=models.CharField(max_length=200,blank=True,verbose_name=u'E-MAIL')
  addedby=models.ForeignKey(User)
  group=models.ForeignKey(Group,verbose_name=u'Группа сертификатов')
  owner=models.ForeignKey(Owner,verbose_name=u'Владелец')
  issuer=models.ForeignKey(Issuer,verbose_name=u'Издатель')
  #area=models.ForeignKey(Area,verbose_name=u'Область действия')
  area=models.ManyToManyField(Area,verbose_name=u'Область действия')
  #type=models.ForeignKey(Type,verbose_name=u'Вид ключевой информации')
  type=models.ManyToManyField(Type,verbose_name=u'Вид ключевой информации')
  skzi=models.ForeignKey(Skzi,verbose_name=u'СКЗИ')

  def __unicode__(self):
    return self.item

class Event(models.Model):
  cert=models.ForeignKey(Cert)
  lasttime=models.DateField(auto_now_add=True)
