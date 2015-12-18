# -*- coding: utf-8 -*-

from django.db import models

class Domain(models.Model):
  name=models.CharField(unique=True,max_length=100,null=False,verbose_name="Домен")
  descr=models.CharField(max_length=100,blank=True,verbose_name="Описание")

  def __unicode__(self):
    return self.name

class User(models.Model):
  email=models.CharField(unique=True,max_length=100,null=False,verbose_name="email адрес")
  fullname=models.CharField(max_length=200,blank=True,verbose_name='Имя')
  passwd=models.CharField(max_length=106,verbose_name='Пароль')
  descr=models.CharField(max_length=100,blank=True,verbose_name="Описание")
  domain=models.ForeignKey(Domain,verbose_name="Домен")

  def __unicode__(self):
    return self.email

class Alias(models.Model):
  src=models.CharField(unique=True,max_length=100,null=False,verbose_name='Источник')
  dst=models.TextField(unique=False,null=False,verbose_name='Назначение')
  descr=models.CharField(unique=False,max_length=100,blank=True,null=False,verbose_name='Описание')
  domain=models.ForeignKey(Domain,verbose_name="Домен")

  def __unicode__(self):
    return "{0}->{1}".format(src,dst)
