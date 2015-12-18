# -*- coding: utf8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.views.generic import TemplateView,RedirectView,ListView
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from gibloc.mixins import LoginRequiredMixin
import models,forms,codecs,socket

class WhiteSites(ListView):
  template_name="squidguard/simplelist.html"

  def get_queryset(self,*argv,**kwargs):
    return models.SiteACLs.objects.get(item='whitesites').Site.all()

class SquidGuard(TemplateView):
  template_name='squidguard/view.html'

  def __getip__(self,item):
    ip=None
    if item.item=='LOCAL NETWORK':
      return '10.0.1.0/24'
    else:
      try:
        ip=socket.gethostbyname(item.item)
      except socket.gaierror, e:
        try:
          ip=socket.gethostbyname('%s%s' % (item.item,item.postlink))
        except socket.gaierror, e:
          raise socket.gaierror(e)
    return ip

  def post(self,request,*args,**kwargs):
    return self.render_to_response(self.get_context_data(**kwargs))

  def get_context_data(self,**kwargs):
    context={'site_acls':models.SiteACLs.objects.all().order_by('item'),
             'host_acls':models.HostACLs.objects.all().order_by('item'),
            }
    action=self.request.POST.get('action')
    if action=='export':
      self.export()
    return context

  def export(self):
    objs=models.SiteACLs.objects.all()
    dest=[]
    src=[]
    acl=['alc {\n']
    for obj in objs:
      #none и all - служебные группы, соответственно их игнорировать при описании групп
      if not (obj.item=='none' or obj.item=='all'):
        with codecs.open('%s.domainlist' % obj.item,'w', encoding='utf-8') as dlist:
          dest.append('dest %s{\n\tdomainlist\t%s\n\tredirect\thttp://www2.gib.ru/empty.gif\n\tlog\t\t%s_access.log\n}\n\n' % (obj.item,dlist.name,obj.item))
          for item in obj.Site.all():
            dlist.write('%s\n' % (item.item))
    objs=models.HostACLs.objects.all()
    for obj in objs:
      src.append('src %s{\n' % obj.item)
      acl.append('\t%s{\n\t\tpass\t' % (obj.item))
      for item in obj.Host.all():
        try:
          ip=self.__getip__(item)
        except socket.gaierror,e:
          #Сообщение в лог
          print 'socket error: %s for hostname: \'%s\'' % (e,item.item)
          continue
        else:
          src.append('\t#%s:%s\n\tip\t%s\n' % (item.item,item.descr,ip))
      src.append('}\n\n')
      for item in obj.SiteACLs_deny.all():
        acl.append('!%s ' % item.item)
      for item in obj.SiteACLs_allow.all():
        acl.append('%s ' % item.item)
      acl.append('\n\t}')
    acl.append('\n}\n')
    with codecs.open('squidguard.conf','w',encoding='utf-8') as sgconf:
      sgconf.writelines(dest)
      sgconf.writelines(src)
      sgconf.writelines(acl)

class SquidGuardDetail(LoginRequiredMixin,SquidGuard):

  def __rget__(self,obj,path):
    try:
      step=path.pop(0)
    except IndexError:
      return obj
    try:
      obj=getattr(obj,step)
    except AttributeError,e:
      try:
        obj=obj.objects.get(item=step)
      except AttributeError,e:
        obj=obj.get(item=step)
    return self.__rget__(obj,path)

  def add(self,obj,item,descr):
    toadd=obj.model(item=item,descr=descr)
    obj.model.save(toadd)
    try:
      obj.add(toadd)
    except IntegrityError,e:
      #Сообщение в лог
      return

  def delete(self,obj,select):
    for item in select:
      try:
        todel=obj.get(item=item)
      except ObjectDoesNotExist,e:
        #Сообщение в лог
        return
      obj.remove(todel)

  def get_context_data(self,**kwargs):
    context=super(SquidGuardDetail,self).get_context_data(**kwargs)
    #Получить obj основываясь на пути path
    path=self.request.path.lstrip('/squidguard').rstrip('/').split('/')
    obj=self.__rget__(models,path[:])
    #Выполнить action
    action=self.request.POST.get('action')
    if action=='add':
      item=self.request.POST.get('item')
      descr=self.request.POST.get('descr')
      self.add(obj,item,descr)
    elif action=='delete':
      select=self.request.POST.getlist('select')
      self.delete(obj,select)
    elif action=='export':
      self.export()
    #Подготовить context для шаблона
    context['m2mf']=obj.model.m2mf
    context['prelink']=obj.model.prelink
    context['postlink']=obj.model.postlink
    try:
      context['form']=getattr(forms,path[-1])
    except AttributeError,e:
      context['form']=None
    context['members']=obj.all().order_by('item')
    return context
