# -*- coding:utf8 -*-

from django.views.generic import UpdateView,DetailView,TemplateView,ListView
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import FormMixin,ProcessFormView,CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect,render_to_response
from gibloc.mixins import LoginRequiredMixin
import codecs,socket,datetime,logging
import models,forms

logger=logging.getLogger(__name__)

class Nothing(LoginRequiredMixin,ListView):
  template_name='licenses/list.html'

  def get_queryset(self):
    return models.Owner.objects.all().order_by('registration')

  def get_context_data(self,**kwargs):
    kwargs['member']='Owner'
    return super(Nothing,self).get_context_data(**kwargs)

class List(LoginRequiredMixin,CreateView):
  template_name='licenses/list.html'

  def dispatch(self,request,*args,**kwargs):
    model=getattr(models,kwargs.get('model'))
    self.member=getattr(models,model.member)
    self.group=model.objects.get(pk=kwargs.get('pk'))
    self.form_class=getattr(forms,model.member)
    self.success_url=request.path
    self.initial['group']=self.group
    return super(List,self).dispatch(request,*args,**kwargs)

  def get_context_data(self,**kwargs):
    kwargs['member']=self.member.__name__
    kwargs['object_list']=self.get_queryset()
    return super(List,self).get_context_data(**kwargs)

  def get_queryset(self):
    return self.member.objects.filter(group=self.group)

  def post(self,request,*args,**kwargs):
    if request.POST.get('action')=='Delete':
      self.delete(request.POST.getlist('selected'))
      return redirect(request.path)
    return super(List,self).post(request,*args,**kwargs)

  def delete(self,selected):
    objs=self.member.objects
    for i in selected:
      objs.get(pk=i).delete()

class Create(LoginRequiredMixin,CreateView):
  template_name='licenses/create.html'

  def dispatch(self,request,*args,**kwargs):
    self.form_class=getattr(forms,kwargs.get('model'))
    self.success_url=request.path
    return super(Create,self).dispatch(request,*args,**kwargs)

class Detail(LoginRequiredMixin,DetailView):

  def dispatch(self,request,*args,**kwargs):
    self.model=getattr(models,kwargs.get('model'))
    self.pk=kwargs.get('pk')
    return super(Detail,self).dispatch(request,*args,**kwargs)

  def get_object(self):
    return self.model.objects.get(pk=self.pk)

class DetailOfLicense(Detail):
  template_name='licenses/detailoflicense.html'

  def get_context_data(self,**kwargs):
    if not kwargs.get('object').owner:
      kwargs['owners']={}
      for g in models.OwnerG.objects.all():
        owners=models.Owner.objects.filter(group=g)
        if owners:
          kwargs['owners'][g]=owners
    return super(DetailOfLicense,self).get_context_data(**kwargs)

  def post(self,request,*args,**kwargs):
    lic=self.get_object()
    if request.POST.get('action')=='attach':
      own=models.Owner.objects.get(pk=request.POST.get('selected'))
      if own:
        lic.owner=own
        lic.save()
    elif request.POST.get('action')=='release':
      lic.owner=None
      lic.save()
    kwargs['object']=lic
    return super(DetailOfLicense,self).get(request,*args,**kwargs)

class DetailOfOwner(Detail):
  template_name='licenses/detailofowner.html'

  def get_context_data(self,**kwargs):
    kwargs['my_inuse']={}
    for obj in models.License.objects.filter(owner=kwargs['object']):
      try:
        kwargs['my_inuse'][obj.group].append(obj)
      except KeyError,e:
        kwargs['my_inuse'][obj.group]=[obj,]
    kwargs['not_inuse']={}
    for group in models.LicenseG.objects.all():
      kwargs['not_inuse'][group]=models.License.objects.filter(group=group,owner__isnull=True)
    return super(DetailOfOwner,self).get_context_data(**kwargs)

  def post(self,request,*args,**kwargs):
    if request.POST.get('action')=='release':
      selected=request.POST.getlist('selected')
      if selected:
        self.release(selected)
    elif request.POST.get('action')=='add':
      selected=request.POST.getlist('selected_toadd')
      if selected:
        self.add(selected)
    return super(DetailOfOwner,self).get(request,*args,**kwargs)

  def release(self,selected):
    for pk in selected:
      lic=models.License.objects.get(pk=pk)
      lic.owner=None
      lic.save()

  def add(self,selected):
    object=self.get_object()
    for i in selected:
      lic=models.License.objects.get(pk=i)
      lic.owner=object
      lic.save()

class ReportOfLicense(Detail):
  template_name=''
  templates={'CryptoPro39':'licenses/reportoflicensecryptopro.html',
             'CryptoPro36':'licenses/reportoflicensecryptopro.html',
             'CryptoPro30':'licenses/reportoflicensecryptopro.html',
             'notfound':'licenses/notfound.html'
            }

  def get_object(self):
    obj=super(ReportOfLicense,self).get_object()
    self.template_name=self.templates.get(str(obj.group),'notfound')
    return obj

#class Import(TemplateView):
#  template_name='licenses/import.html'
#
#  def get_context_data(self,*args,**kwargs):
#    kwargs['LicenseG']=models.LicenseG.objects.all().order_by('item')
#    kwargs['OwnerG']=models.OwnerG.objects.all().order_by('item')
#    return super(Import,self).get_context_data(*args,**kwargs)
#
#  def post(self,request,*args,**kwargs):
#    from datetime import datetime
#    lfile=request.FILES.get('lfile')
#    ofile=request.FILES.get('ofile')
#    od={}
#    ownergroup=models.OwnerG.objects.get(item='Clients')
#    for o in ofile:
#      o=o.strip()
#      o=o.split(',')
#      od[o[1]]=o[0]
#    for l in lfile:
#      l=l.strip()
#      l=l.split(',')
#      if l[2]=='CryptoPro30':
#        descr=u'Крипто Про CSP 3.0'
#      else:
#        descr=u'Крипто Про CSP 3.6'
#      licgroup=models.LicenseG.objects.get(item=l[2])
#      try:
#        orgname=od[l[0]]
#      except KeyError:
#        owner=None
#      else:
#        owner=models.Owner(item=orgname,group=ownergroup)
#        try:
#          owner.save()
#        except:
#          owner=models.Owner.objects.get(item=orgname)
#      license=models.License(item=l[1],descr='',changestate=datetime.now(),owner=owner,group=licgroup)
#      license.save()
#    return super(Import,self).get(request,*args,**kwargs)

