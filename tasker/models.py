# -*- coding: utf8 -*-

from django.contrib.auth.models import User as Person
from django.db import models
import datetime
import actions,repeat

class TaskG(models.Model):
  name=models.CharField(max_length=20,unique=True)
  description=models.CharField(max_length=100,blank=True)
  email=models.CharField(max_length=200,blank=True)
  member='Task'

  def __unicode__(self):
    return self.name

class Task(models.Model):
  choices=(('1',u'Новое'),
           ('2',u'Нихера непонятно'),
           ('3',u'В работе'),
           ('4','4!'),
           ('5','5!'),
           ('6','6!'),
           ('7','7!'),
           ('8','8!'),
           ('9',u'Отменено'),
           ('10',u'Завершено'),
          )
  notactive=(u'Завершено',
             u'Отменено',
            )
  name=models.CharField(max_length=20)
  description=models.CharField(max_length=100,blank=True)
  text=models.TextField(blank=True)
  addtime=models.DateField(auto_now_add=True)
  starttime=models.DateField(blank=True,null=True)
  #deadtime=models.DateField(blank=True,null=True)
  deadtime=models.DateField(default=datetime.datetime.max)
  repeat=models.IntegerField(choices=repeat.repeat.as_list(),blank=True,null=True)
  nday=models.IntegerField(blank=True,null=True)
  action=models.IntegerField(choices=actions.actions.as_list(),blank=True,null=True)
  email=models.CharField(max_length=200,blank=True)
  private=models.BooleanField(default=False)
  owner=models.ForeignKey(Person,related_name='task_person_owner')
  performer=models.ForeignKey(Person,related_name='task_person_performer')
  group=models.ForeignKey(TaskG)
  state=models.CharField(max_length=10,choices=choices)

  class Meta():
    ordering=['-addtime']

  def __unicode__(self):
    return self.name

class Event(models.Model):
  task=models.ForeignKey(Task)
  lasttime=models.DateField(auto_now_add=True)

class Comment(models.Model):
  owner=models.ForeignKey(Person)
  comment=models.TextField()
  addtime=models.DateTimeField(auto_now_add=True)
  task=models.ForeignKey(Task)

  class Meta():
    ordering=['-addtime']

  def __unicode__(self):
    return self.comment
