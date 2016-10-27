# -*- coding: utf8 -*-

from choice import Choices
from datetime import timedelta,date
import models
import actions

class EveryNDay(object):
  name=u'Каждый N день'

  def __init__(self,obj):
    self.obj=obj
    events=models.Event.objects.filter(task=obj)
    self.deadtime=obj.deadtime
    self.lasttime=events.latest('lasttime').lasttime if events else obj.starttime if obj.starttime else obj.addtime
    self.nexttime=self.get_nexttime(self.lasttime,obj.nday)
    self.today=date.today()

  def get_nexttime(self,lasttime,nday):
    return lasttime+timedelta(days=nday)

  def le_date(self,x,y):
    if not isinstance(y,date):
      return True
    else:
      return x<=y

  def __call__(self):
    state_text=self.obj.choices[int(self.obj.state)-1][1]
    isactive=False if state_text in self.obj.notactive else True
    if isactive and self.obj.action:
      #print "--------"
      #print 'task=%s, lastime=%s, deadtime=%s, nday=%s, nexttime=%s'%(self.obj,self.lasttime,self.deadtime,self.obj.nday,self.nexttime)
      #if ((self.nexttime<=self.today and self.nexttime<=self.deadtime) or
      if ((self.nexttime<=self.today and self.le_date(self.nexttime,self.deadtime)) or
          self.lasttime==self.today or
          (self.deadtime and self.deadtime==self.today)):
        #print 'task=%s, lastime=%s, deadtime=%s, nday=%s, nexttime=%s'%(self.obj,self.lasttime,self.deadtime,self.obj.nday,self.nexttime)
        action=actions.actions.get_choice(self.obj.action)(self.obj)
        try:
          action()
          pass
        except Exception,e:
          print e
          pass
        else:
          if not models.Event.objects.filter(lasttime=self.today,task=self.obj):
            event=models.Event(task=self.obj,lasttime=self.today)
            event.save()

class EveryNDayOfWeek(EveryNDay):
  name=u'Каждый N день недели'
  def get_nexttime(self,lasttime,nday):
    nday-=1
    if nday>6: nday=6
    delta=nday-lasttime.weekday()
    return lasttime+timedelta(days=delta) if delta>0 else lasttime+timedelta(days=7+delta)

class EveryNDayOfMonth(EveryNDay):
  name=u'Каждый N день месяца'

  def get_nexttime(self,lasttime,nday):
    day=nday
    lday=lasttime.day
    month=lasttime.month-1
    if(month==11):year=lasttime.year+1
    else:year=lasttime.year
    maxdays=[31,28,31,30,31,30,31,31,30,31,30,31]
    #Проверка на високосность
    if (year%4 and not year%100) or (year%400):
      maxdays[1]=29
    #Если day превышает колличество дней в месяце
    if day>maxdays[month]: day=maxdays[month]
    if lday<day: return lasttime.replace(day=day) #время события ещё не наступило
    else: #След. месяц
      month=0 if month==11 else month+1 #след. месяц
      if nday>maxdays[month]: return lasttime.replace(month=month+1,day=maxdays[month],year=year)
      else: return lasttime.replace(month=month+1,day=nday,year=year)
            

repeat=Choices()
repeat.register(EveryNDay)
repeat.register(EveryNDayOfWeek)
repeat.register(EveryNDayOfMonth)

