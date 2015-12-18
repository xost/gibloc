# -*- coding: utf8 -*-

from django.views.generic import TemplateView,ListView,View,DetailView,FormView
from django.views.generic.edit import CreateView,UpdateView
from django.shortcuts import redirect
from django.db.models import Q
import datetime
import models,forms
import operator

class LMenu(View):
  def get_context_data(self,**kwargs):
    kwargs['lmenu']={'group':models.Group.objects.all(),
                     'owner':models.Owner.objects.all(),
                     'issuer':models.Issuer.objects.all(),
                     'skzi':models.Skzi.objects.all(),
                     'type':models.Type.objects.all(),
                     'area':models.Area.objects.all(),
                    }
    return super(LMenu,self).get_context_data(**kwargs)

class LMenu2(FormView):
  lmenu_form_class=forms.LMenuForm
  template_name='certs/leftmenu.html'

class SimpleView(LMenu,TemplateView):
  template_name='certs/simpleview.html'

class List(LMenu,ListView):
  template_name='certs/list.html'
  err={}
  fltr=False

  def get_context_data(self,**kwargs):
    kwargs['fltr']={'group':self.request.GET.getlist('f_group'),
                    'owner':self.request.GET.getlist('f_owner'),
                    'issuer':self.request.GET.getlist('f_issuer'),
                    'skzi':self.request.GET.getlist('f_skzi'),
                    'type':self.request.GET.getlist('f_type'),
                    'area':self.request.GET.getlist('f_area'),
                   }
    #kwargs['lmenu']=self.lmenu_form_class
    kwargs['f_']=self.request.META.get('QUERY_STRING').split('&sortby')[0].rstrip("&action=Filter")
    kwargs['r_']=self.request.META.get('QUERY_STRING').replace('action=Filter','')
    kwargs['reverse']=not self.reverse
    kwargs['dates']={'startgt':self.startgt,'startlt':self.startlt,'deadgt':self.deadgt,'deadlt':self.deadlt}
    return super(List,self).get_context_data(**kwargs)

  def get_queryset(self,*argv,**kwargs):
    qs=models.Cert.objects.all()
    if self.fltr:
      for f in self.fltr:
        qlist=[Q(x)for x in f]
        qs=qs.filter(reduce(operator.or_,qlist))
      qs=qs.order_by(self.sortby)
    else:
      qs=models.Cert.objects.all().order_by(self.sortby)
    if self.startgt and self.startlt:
      qs=qs.filter(starttime__gt=self.startgt,starttime__lt=self.startlt)
    elif self.startgt:
       qs=qs.filter(starttime__gt=self.startgt)
    elif self.startlt:
       qs=qs.filter(starttime__lt=self.startlt)
    if self.deadgt and self.deadlt:
      qs=qs.filter(deadtime__gt=self.deadgt,deadtime__lt=self.deadlt)
    elif self.deadgt:
       qs=qs.filter(deadtime__gt=self.deadgt)
    elif self.deadlt:
       qs=qs.filter(deadtime__lt=self.deadlt)
    if self.reverse:
      qs=qs.reverse()
    return qs

  def get(self,request,*argv,**kwargs):
    self.reverse=True if self.request.GET.get('reverse','False')=='True' else False
    self.sortby=request.GET.get('sortby','deadtime')
    try:
      self.startgt=datetime.datetime.strptime(request.GET.get('startgt'),'%d/%m/%Y').date() if request.GET.get('startgt') else ''
    except ValueError,e:
      self.err['startgt']=('Неверный формат даты')
      raise ValueError(e)
    try:
      self.startlt=datetime.datetime.strptime(request.GET.get('startlt'),'%d/%m/%Y').date() if request.GET.get('startlt') else ''
    except ValueError,e:
      self.err['startlt']=('Неверный формат даты')
      raise ValueError(e)
    try:
      self.deadgt=datetime.datetime.strptime(request.GET.get('deadgt'),'%d/%m/%Y').date() if request.GET.get('deadgt') else ''
    except ValueError,e:
      self.err['deadgt']=('Неверный формат даты')
      raise ValueError(e)
    try:
      self.deadlt=datetime.datetime.strptime(request.GET.get('datelt'),'%d/%m/%Y').date() if request.GET.get('deadlt') else ''
    except ValueError,e:
      self.err['deadlt']=('Неверный формат даты')
      raise ValueError(e)
    action=request.GET.get('action')
    if action=='Create':
      return redirect('/certs/create/Cert')
    elif action=='Delete':
      for delete in self.request.GET.getlist('delete'):
        models.Cert.objects.get(pk=delete).delete()
    elif action=='Filter' or action=='Report' :
      #выбрать параметры в GET запросе начинающиеся с "f_"
      f_=(filter(lambda x: x.startswith('f_'),request.GET.keys()))
      self.fltr=[]
      for q in f_:
        #отмести ведущую "f_", получив тем самым поле в модели Cert
        f_strip=q.lstrip('f_')
        #сформировать список вида [[('attr1',obj11)('attr1',obj12)],[('attr2',obj21)]]
        self.fltr.append(map(lambda x:(f_strip,getattr(models,f_strip.capitalize()).objects.get(pk=x)),request.GET.getlist(q)))
      if action=='Report':
        self.template_name='certs/report.html'
    return super(List,self).get(request,*argv,**kwargs)

class Create(LMenu,CreateView):
  template_name='certs/edit.html'
  success_url='/certs/list'

  def dispatch(self,*argv,**kwargs):
    #self.from_class на основании url (/certs/"model")
    self.form_class=getattr(forms,kwargs.get('model'))
    return super(Create,self).dispatch(*argv,**kwargs)

  def form_valid(self,form):
    form.instance.addedby=self.request.user
    return super(Create,self).form_valid(form)

class Detail(LMenu,DetailView):
  template_name='certs/detail.html'
  model=models.Cert

  def post(self,request,*argv,**kwargs):
    if request.POST.get('action')=='Edit':
      return redirect('/certs/edit/%s'%self.kwargs.get('pk'))

class Edit(LMenu,UpdateView):
  template_name='certs/edit.html'
  form_class=forms.Cert
  success_url='/certs/list'

  def get_object(self):
    return models.Cert.objects.get(pk=self.kwargs.get('pk'))

class Report(List):
  template_name='certs/report.html'
