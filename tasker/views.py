# -*- coding:utf8 -*-

from django.shortcuts import get_object_or_404,redirect
from django.views.generic import TemplateView,View,DetailView,ListView
from django.views.generic.edit import CreateView,UpdateView,FormMixin
from django.db.models import Q
from gibloc.mixins import LoginRequiredMixin
import models,forms

class SimpleView(TemplateView):
  template_name='tasker/simpleview.html'
  pass

  def get_context_data(self,**kwargs):
    kwargs['lmenu']=models.TaskG.objects.all()
    return super(SimpleView,self).get_context_data(**kwargs)

class LMenu(View):
  def get_context_data(self,**kwargs):
    kwargs['lmenu']=models.TaskG.objects.all()
    return super(LMenu,self).get_context_data(**kwargs)

class ListOf(LoginRequiredMixin,LMenu,ListView):
  def get_queryset(self,*argv,**kwargs):
    group=getattr(models,self.kwargs['model'])
    model=getattr(models,group.member)
    q=model.objects.filter(Q(group=group.objects.get(id=self.kwargs['pk'])),
                           Q(performer=self.request.user)|
                           Q(owner=self.request.user)|
                           Q(private=False)).order_by(self.order_by)
    if self.reverse:
      return q.reverse()
    else:
      return q

  def post(self,request,*argv,**kwargs):
    if request.POST.get('submit')=='Delete':
      for i in request.POST.getlist('select'):
        getattr(models,getattr(models,self.kwargs['model']).member).objects.get(pk=i).delete()
    #return super(ListOf,self).get(request,*argv,**kwargs)
    return self.get(request,*argv,**kwargs)

  def get(self,request,*argv,**kwargs):
    self.order_by=request.GET.get('order_by','addtime')
    self.reverse=False if request.GET.get('reverse','True')=='False' else True
    return super(ListOf,self).get(request,*argv,**kwargs)

  def get_context_data(self,**kwargs):
    kwargs['reverse']=not self.reverse
    return super(ListOf,self).get_context_data(**kwargs)

class ListOfTask(ListOf):
  template_name='tasker/listoftask.html'

  def get_context_data(self,**kwargs):
    kwargs['TaskG']=self.kwargs['pk']
    return super(ListOfTask,self).get_context_data(**kwargs)

class DetailOf(LoginRequiredMixin,LMenu,DetailView):
  def get_queryset(self):
    return getattr(models,self.kwargs['model']).objects.all()

class DetailOfTask(LoginRequiredMixin,LMenu,CreateView):
  template_name='tasker/detailoftask.html'
  form_class=forms.Comment

  def get_context_data(self,**kwargs):
    kwargs['object']=models.Task.objects.get(pk=self.kwargs['pk'])
    kwargs['comments']=models.Comment.objects.filter(task=kwargs['object'])
    return super(DetailOfTask,self).get_context_data(**kwargs)

  def get_success_url(self):
    return self.request.path

  def post(self,request,*argv,**kwargs):
    action=request.POST.get('submit')
    if action=='add':
      return super(DetailOfTask,self).post(request,*argv,**kwargs)
    elif  action=='delete':
      for i in request.POST.getlist('select'):
        models.Comment.objects.get(pk=i).delete()
    return redirect(self.get_success_url())

  def form_valid(self,form):
    form.instance.owner=self.request.user
    form.instance.task=models.Task.objects.get(pk=self.kwargs['pk'])
    return super(DetailOfTask,self).form_valid(form)

class Create(LoginRequiredMixin,LMenu,CreateView):
  template_name='tasker/create.html'
  def dispatch(self,request,*args,**kwargs):
    self.form_class=getattr(forms,kwargs.get('model'))
    self.success_url=request.path
    return super(Create,self).dispatch(request,*args,**kwargs)

class CreateTask(LoginRequiredMixin,LMenu,CreateView):
  template_name='tasker/createtask.html'
  form_class=forms.Task

  def get_success_url(self):
    return '/tasker/detailof/Task/%s'% self.object.pk

  def get_queryset(self):
    group=getattr(models,self.kwargs['model'])
    return getattr(models,group.member).objects.all()

  def form_valid(self,form):
    form.instance.owner=self.request.user
    form.instance.group=getattr(models,self.kwargs['model']).objects.get(pk=self.kwargs['pk'])
    return super(CreateTask,self).form_valid(form)

class Edit(LoginRequiredMixin,LMenu,UpdateView):

  def get_success_url(self):
    return '/tasker/detailof/Task/%s' % self.object.pk

  def get_object(self):
    model=getattr(models,self.kwargs['model'])
    self.form_class=getattr(forms,self.kwargs['model'])
    return get_object_or_404(model,pk=self.kwargs['pk'])

class EditTask(Edit):
  template_name='tasker/edittask.html'
