from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.views.generic import TemplateView,ListView
from gibloc.mixins import LoginRequiredMixin
import models,forms
import codecs,socket

class WiteSitesList(ListView):
  template_name='squid/list.html'

  def get_queryset(self,request,*argv,**kwargs):
    pass

class Squid(LoginRequiredMixin,TemplateView):
  template_name='squid/view.html'

  def get_context_data(self,**kwargs):
    context={'host_acls':models.HostACLs.objects.all().order_by('name'),
             'port_acls':models.PortACLs.objects.all().order_by('name'),
             'url_acls':models.UrlACLs.objects.all().order_by('name'),
            }
    return context

class SquidDetail(Squid):
  def add(self,**kwargs):
    item=kwargs.get('item')
    descr=kwargs.get('descr')
    obj=kwargs.get('obj')
    model=kwargs.get('model')
    try:
      toadd=getattr(models,model).objects.create(item=item,descr=descr)
    except IntegrityError,e:
      toadd=getattr(models,model).objects.get(item=kwargs.get('item'))
      toadd.descr=descr
      toadd.save()
    obj.items.add(toadd)

  def delete(self,**kwargs):
    selected=kwargs.get('selected')
    obj=kwargs.get('obj')
    model=kwargs.get('model')
    for item in selected:
      todel=getattr(models,model).objects.get(item=item)
      obj.items.remove(todel)

  def export(self,**kwargs):
    model_list=('HostACLs','PortACLs','UrlACLs')
    errors=[]
    messages=[]
    for model in model_list:
      for obj in getattr(models,model).objects.all():
        fname='%s.%s' % (model.strip('ACLs').lower(),obj)
        try:
          fh=codecs.open(fname,'w','utf-8')
          for item in obj.items.all():
            if hasattr(item,'error'):
              errors.append(item.error)
              continue
            elif hasattr(item,'alt'):
              descr='%s - %s' % (item.item,item.descr)
              fh.write('#%s\n%s\n' % (descr,item.alt))
            else:
              descr=item.descr
              fh.write('#%s\n%s\n' % (descr,item.item))
        except IOError,e:
          errors.append('IOError: %s' % e)
    if errors:
      messages.append('Export with errors.')
    else:
      messages.append('Export was successfull.')
    return (messages,errors)

  def get_context_data(self,**kwargs):
    context=super(SquidDetail,self).get_context_data(**kwargs)
    model=kwargs.get('model')
    acl=kwargs.get('acl')
    request=self.request
    action=request.GET.get('action')
    if model:
      mode=model+'ACLs'
      form=model+'Form'
      obj=getattr(models,mode).objects.get(name=acl)
      context['members']=obj.items.all()
      context['form']=getattr(forms,form)
    if action and obj:
      get_args={'obj':obj,'model':model,'item':request.GET.get('item'),'descr':request.GET.get('descr'),'selected':request.GET.getlist('select')}
      getattr(self,action)(**get_args)
    return context
