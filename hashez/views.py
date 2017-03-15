# -*- coding: utf8 -*-

from django.shortcuts import render
from django.views.generic import ListView,TemplateView,DetailView
import models

# Create your views here.

class Simple(TemplateView):
  template_name="hashez/simple.html"

class EventList(ListView):
  template_name='hashez/events.html'

  def dispatch(self,request,*args,**kwargs):
    self.clientId=kwargs.get('pk')
    return super(EventList,self).dispatch(request,*args,**kwargs)
  
  def get_queryset(self):
    return models.Event.objects.filter(client_id=self.clientId)

class ClientDetail(DetailView):
  template_name='hashez/clientDetail.html'
  model=models.Client
  clientId=0

  def dispatch(self,request,*args,**kwargs):
    self.clientId=kwargs.get('pk')
    return super(ClientDetail,self).dispatch(request,*args,**kwargs)

  def get_context_data(self,**kwargs):
    fileSets=models.FileSet.objects.filter(client_id=self.clientId)
    fileSet=fileSets.latest('pk')
    events=models.Event.objects.filter(client_id=self.clientId)
    files=models.File.objects.filter(fileSet=fileSet)
    kwargs['fileSets']=fileSets
    kwargs['events']=events
    kwargs['files']=files
    return super(ClientDetail,self).get_context_data(**kwargs)
