from django.shortcuts import get_object_or_404,redirect
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView,UpdateView
from django.db.models import Q
from gibloc.mixins import LoginRequiredMixin
import hashlib
import models,forms

class Nothing(TemplateView):
  pass

class Create(LoginRequiredMixin,CreateView):
  template_name='mail/create.html'
  def dispatch(self,request,*args,**kwargs):
    model=kwargs.get('model')
    self.form_class=getattr(forms,model)
    self.success_url='/mail/create/{0}'.format(model)
    return super(Create,self).dispatch(request,*args,**kwargs)

class List(LoginRequiredMixin,CreateView):
  fltr=''
  template_name='mail/list.html'

  def dispatch(self,request,model='User',pk='1'):
    self.model=model
    self.pk=pk
    self.domain=models.Domain.objects.get(pk=self.pk)
    if not self.model:
      self.model='User';
    if self.pk and not self.pk=='None':
      self.initial['domain']=self.domain
    self.template_name='mail/list_{0}.html'.format(self.model)
    self.form_class=getattr(forms,self.model)
    return super(List,self).dispatch(request,model,pk)

  def post(self,*args,**kwargs):
    self.action=self.request.POST.get('action')
    self.success_url='/mail/list/{0}/{1}'.format(self.model,self.pk)
    return super(List,self).post(*args,**kwargs)

  def form_invalid(self,form):
    if self.action=='Delete':
      self.delete(self.request.POST.getlist('selected'))
      form.errors.clear()
    elif self.action=='Filter':
      self.fltr=self.request.POST.get('fltr')
      form.errors.clear()
    return super(List,self).form_invalid(form)

  def form_valid(self,form):
    if hasattr(form.instance,'passwd'):
      passwd=form.instance.passwd
      form.instance.passwd='''{PLAIN-MD5}'''+hashlib.md5(passwd).hexdigest()
    return super(List,self).form_valid(form)

  def get_context_data(self,*args,**kwargs):
    kwargs['object_list']=self.get_queryset()
    kwargs['form_filter']=forms.Filter({'fltr':self.fltr})
    return super(List,self).get_context_data(*args,**kwargs)

  def get_queryset(self,*args,**kwargs):
    if self.fltr:
      qs=getattr(models,self.model).objects.filter(Q(email__icontains=self.fltr)|
                                                   Q(fullname__icontains=self.fltr)|
                                                   Q(descr__icontains=self.fltr),
                                                   Q(domain=self.domain))
    else:
      qs=getattr(models,self.model).objects.filter(domain=self.domain);
    return qs

  def delete(self,selected):
    for pk in selected:
      getattr(models,self.model).objects.get(pk=pk).delete()

class Update(LoginRequiredMixin,UpdateView):
  template_name='mail/update.html'

  def get_success_url(self):
    domain=self.model.objects.get(pk=self.pk).domain.pk
    return '/mail/list/{0}/1/'.format(self.model.__name__,domain)

  def get_object(self):
    self.model=getattr(models,self.kwargs['model'])
    self.pk=self.kwargs.get('pk')
    self.form_class=getattr(forms,self.kwargs.get('model'))
    return get_object_or_404(self.model,pk=self.pk)

  def form_valid(self,form):
    if hasattr(form.instance,'passwd'):
      passwd=form.instance.passwd
      form.instance.passwd='''{PLAIN-MD5}'''+hashlib.md5(passwd).hexdigest()
    return super(Update,self).form_valid(form)
