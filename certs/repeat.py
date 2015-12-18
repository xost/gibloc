# -*- coding: utf8 -*-

from choice import Choices
from datetime import timedelta,date
import models
import actions,repeat

class BeforeDeadNDay(object):
  name=u'За N дней до окончания срока действия'

  def __init__(self,obj):
    self.obj=obj
    self.events=models.Event.objects.filter(cert=obj)
    self.deadtime=obj.deadtime
    self.lasttime=self.events.latest('lasttime').lasttime if self.events else None

  def __call__(self):
    d=self.obj.deadtime-date.today()
    if d.days>=0 and d.days<=self.obj.nday:
      action=actions.actions.get_choice(self.obj.action)(self.obj)
      action()
      #try:
      #  action()
      #except:
      #  print 'Error send message'
      #else:
      #  models.Event(cert=self.obj).save()

repeat=Choices()
repeat.register(BeforeDeadNDay)
