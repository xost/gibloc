# -*- coding: utf8 -*-

from django.shortcuts import render
from django.views.generic import ListView,TemplateView
import models 

# Create your views here.

class Simple(TemplateView):
  template_name="hashez/simple.html"

class EventList(ListView):
  template_name='hashez/events.html'
  clientId=0

  def dispatch(self,request,*args,**kwargs):
    self.clientId=kwargs.get('pk')
    return super(EventList,self).dispatch(request,*args,**kwargs)
  
  def get_queryset(self):
    return models.Event.objects.filter(client_id=self.clientId)
