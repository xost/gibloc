# -*- coding:utf8 -*-

from django.views.generic import DetailView,TemplateView,ListView
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import FormMixin,ProcessFormView,CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from gibloc.mixins import LoginRequiredMixin
import codecs,socket,datetime,logging
import models,forms

logger=logging.getLogger(__name__)

class LicenseView(TemplateView):
  template_name='licenses/simpleview.html'

  def get_context_data(self,**kwargs):
    kwargs['LicenseACL']=models.LicenseACL.objects.all().order_by('item')
    kwargs['OwnerACL']=models.OwnerACL.objects.all().order_by('item')
    return super(LicenseView,self).get_context_data(**kwargs)

class ListOf(LoginRequiredMixin,FormMixin,ListView):
  template_name='licenses/listof.html'

  def get_context_data(self,**kwargs):
    context=super(ListOf,self).get_context_data(**kwargs)
    context['LicenseACL']=models.LicenseACL.objects.all().order_by('item')
    context['OwnerACL']=models.OwnerACL.objects.all().order_by('item')
    context['form']=self.get_form(self.form_class)
    context['member']=getattr(models,self.model)().member().__class__.__name__
    context['reverse']=not self.reverse
    return context

  def get_queryset(self,*args,**kwargs):
    if self.model and self.acl:
      obj=getattr(models,self.model)()
      queryset=obj.member.objects.filter(acl=self.acl).order_by(self.order_by).reverse()
      if self.reverse:
        return queryset.reverse()
      else:
        return queryset
    return []

  def get(self,request,*args,**kwargs):
    self.model=self.kwargs.get('model')
    self.acl=self.kwargs.get('acl')
    self.order_by=request.GET.get('order_by','item')
    self.reverse=request.GET.get('reverse',False)
    self.reverse=False if self.reverse=='False' else True
    return super(ListOf,self).get(request,*args,**kwargs)

  def post(self,request,*args,**kwargs):
    self.model=self.kwargs.get('model')
    self.acl=self.kwargs.get('acl')
    form_class=self.get_form_class()
    form=self.get_form(form_class)
    action=request.POST.get('action')
    self.success_url='/licenses/listof/%s/%s' % (self.model,self.acl)
    if action=='add':
      if form.is_valid():
        return self.form_valid(form)
      else:
        return self.form_invalid(form)
    elif action=='delete':
      selected=request.POST.getlist('selected')
      self.delete(selected)
      return super(ListOf,self).form_valid(form)

  def delete(self,selected):
    obj=getattr(models,self.model)()
    for i in selected:
      license=obj.member.objects.get(id=i)
      logger.info('Удалена: %s' % license)
      license.delete()

class ListOfLicense(ListOf):
  form_class=forms.License

  def form_valid(self,form):
    from copy import copy
    obj=form.save(commit=False)
    acl=getattr(models,self.model).objects.get(item=self.acl)
    obj.acl=acl
    for i in xrange(form.cleaned_data['number']):
      new_obj=copy(obj)
      new_obj.inuse=False
      new_obj.save()
      logger.info('Зарегистрирована лицензия: %s (%d)' % (new_obj,i))
    return super(ListOf,self).form_valid(form)

class ListOfOwner(ListOf):
  form_class=forms.Owner

  def form_valid(self,form):
    obj=form.save(commit=False)
    acl=getattr(models,self.model).objects.get(item=self.acl)
    obj.acl=acl
    obj.save()
    logger.info('Зарегистрирован: %s' % obj)
    return super(ListOf,self).form_valid(form)

  def form_invalid(self,form):
    print form.as_p()

  def delete(self,selected):
    acl=getattr(models,self.model)()
    for i in selected:
      obj=acl.member.objects.get(pk=i)
      for l in models.License.objects.filter(owner=obj):
        l.owner=None
        l.inuse=False
        l.changestate=datetime.datetime.now()
        l.save()
      obj.delete()

class DetailOf(LoginRequiredMixin,DetailView):

  def get_context_data(self,**kwargs):
    kwargs['LicenseACL']=models.LicenseACL.objects.all().order_by('item')
    kwargs['OwnerACL']=models.OwnerACL.objects.all().order_by('item')
    return super(DetailOf,self).get_context_data(**kwargs)

  def get_object(self,*args,**kwargs):
    id_=self.kwargs.get('id')
    self.model=getattr(models,self.kwargs.get('model'))
    return self.model.objects.get(id=id_)

class DetailOfLicense(DetailOf):
  template_name='licenses/detailoflicense.html'
  model=models.License

  def get_context_data(self,**kwargs):
    try:
      kwargs['owner_id']=kwargs['object'].owner.id
    except AttributeError,e:
      kwargs['owner_id']=None
    kwargs['owners']={}
    for acl in models.OwnerACL.objects.all():
      objects=models.Owner.objects.filter(acl=acl)
      if objects:
        kwargs['owners'][acl]=objects
    return super(DetailOfLicense,self).get_context_data(**kwargs)

  def post(self,request,*args,**kwargs):
    if request.POST.get('action')=='release':
      obj=self.get_object(*args,**kwargs)
      owner=obj.owner
      obj.owner=None
      obj.inuse=False
      obj.changestate=datetime.datetime.now()
      obj.save()
      logger.info('С %s снята лицензия %s' % (owner,obj))
    else:
      id_=request.POST.get('selected')
      obj=self.get_object(*args,**kwargs)
      attach=models.Owner.objects.get(id=id_)
      obj.owner=attach
      obj.inuse=True
      obj.save()
      logger.info('%s назначена лицензия %s' % (attach,obj))
    return super(DetailOfLicense,self).get(request,*args,**kwargs)

class DetailOfOwner(DetailOf):
  template_name="licenses/detailofowner.html"
  model=models.Owner

  def get_context_data(self,*args,**kwargs):
    kwargs['my_inuse']={}
    for obj in models.License.objects.filter(owner=kwargs['object']):
      try:
        kwargs['my_inuse'][obj.acl].append(obj)
      except KeyError,e:
        kwargs['my_inuse'][obj.acl]=[obj,]
    kwargs['not_inuse']={}
    for acl in models.LicenseACL.objects.all():
      kwargs['not_inuse'][acl]=models.License.objects.filter(acl=acl,inuse=False)
    return super(DetailOfOwner,self).get_context_data(*args,**kwargs)

  def post(self,request,*args,**kwargs):
    if request.POST.get('action')=='release':
      for id_ in request.POST.getlist('selected'):
        obj=models.License.objects.get(id=id_)
        owner=obj.owner
        obj.owner=None
        obj.inuse=False
        obj.changestate=datetime.datetime.now()
        obj.save()
        logger.info('С %s снята лицензия %s' % (owner,obj))
    else:
      for id_ in request.POST.getlist('selected_toadd'):
        obj=models.License.objects.get(id=id_)
        obj.owner=self.model.objects.get(id=kwargs['id'])
        obj.inuse=True
        obj.changestate=datetime.datetime.now()
        obj.save()
        logger.info('%s назначена лицензия %s' % (obj.owner,obj))
    return super(DetailOfOwner,self).get(request,*args,**kwargs)

class ReportOfLicense(DetailView):
  template_name=''
  templates={'CryptoPro36':'licenses/reportoflicensecryptopro.html',
             'CryptoPro30':'licenses/reportoflicensecryptopro.html',
             'notfound':'licenses/notfound.html'
            }

  def get_object(self,*args,**kwargs):
    id_=self.kwargs.get('id')
    self.model=getattr(models,self.kwargs.get('model'))
    obj=self.model.objects.get(id=id_)
    self.template_name=self.templates.get(str(obj.acl),'notfound')
    return obj

class LMenu():
  def get_context_data(self,)

class List(LoginRequiredMixin,ListView):
  template_name='licenses/list.html'

  def get_context_data(self,**kwargs):
    kwargs['']
    return super(List,self).get_context_data(**kwargs)

  def dispatch(self,request,*args,**kwargs):
    self.model=
    return super(List,self).dispatch(request,*args,**kwargs)

class Create(LoginRequiredMixin,CreateView):
  template_name='licenses/create.html'

  def get_context_data(self,**kwargs):
    kwargs['LicenseACL']=models.LicenseACL.objects.all().order_by('item')
    kwargs['OwnerACL']=models.OwnerACL.objects.all().order_by('item')
    return super(Create,self).get_context_data(**kwargs)

  def dispatch(self,request,*args,**kwargs):
    self.model=getattr(models,kwargs.get('model'))
    return super(Create,self).dispatch(request,*args,**kwargs)

  def post(self,request):
    if request.POST.get('action')=='Create':
      pass

  def form_valid(self,form):
    self.success_url=self.request.path
    return super(Create,self).form_valid(form)

class Import(TemplateView):
  template_name='licenses/import.html'

  def get_context_data(self,*args,**kwargs):
    kwargs['LicenseACL']=models.LicenseACL.objects.all().order_by('item')
    kwargs['OwnerACL']=models.OwnerACL.objects.all().order_by('item')
    return super(Import,self).get_context_data(*args,**kwargs)

  def post(self,request,*args,**kwargs):
    from datetime import datetime
    lfile=request.FILES.get('lfile')
    ofile=request.FILES.get('ofile')
    od={}
    owneracl=models.OwnerACL.objects.get(item='Clients')
    for o in ofile:
      o=o.strip()
      o=o.split(',')
      od[o[1]]=o[0]
    for l in lfile:
      l=l.strip()
      l=l.split(',')
      if l[2]=='CryptoPro30':
        descr=u'Крипто Про CSP 3.0'
      else:
        descr=u'Крипто Про CSP 3.6'
      licacl=models.LicenseACL.objects.get(item=l[2])
      try:
        orgname=od[l[0]]
      except KeyError:
        owner=None
        inuse=False
      else:
        owner=models.Owner(item=orgname,acl=owneracl)
        try:
          owner.save()
        except:
          owner=models.Owner.objects.get(item=orgname)
        inuse=True
      license=models.License(item=l[1],descr='',inuse=inuse,changestate=datetime.now(),owner=owner,acl=licacl)
      license.save()
    return super(Import,self).get(request,*args,**kwargs)

