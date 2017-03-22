# -*- coding: utf8 -*-

from django.shortcuts import render
from django.views.generic import ListView,TemplateView,DetailView
import models

# Create your views here.

class Simple(TemplateView):
  template_name="hashez/simple.html"

class EventList(ListView):
  template_name='hashez/events.html'
  sqlQuery=""" SELECT E.id,
                      E.eventType,
                      E.result,
                      E.registred,
                      E.fileSet_id,
                      E.badFiles_id,
                      (
                        SELECT count(*)
                        FROM hashez_file F
                        WHERE F.fileSet_id=E.fileSet_id
                      ) as files_count
               FROM hashez_event E
               WHERE E.client_id={0}
               ORDER BY E.id {1}
           """

  def dispatch(self,request,*args,**kwargs):
    self.clientId=kwargs.get('pk')
    self.sort=request.GET.get('sort');
    return super(EventList,self).dispatch(request,*args,**kwargs)
  
  def get_queryset(self):
    events=models.Event.objects.filter(client_id=self.clientId)
    sqlQuery=self.sqlQuery.format(self.clientId,"DESC" if self.sort=="DESC" else "ASC");
    qset=models.Event.objects.raw(sqlQuery)
    return qset

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
    lastEvent=events.latest('pk')
    files=models.File.objects.filter(fileSet=fileSet)
    kwargs['fileSets']=fileSets
    kwargs['lastEvent']=lastEvent
    kwargs['files']=files
    return super(ClientDetail,self).get_context_data(**kwargs)

class FileSet(ListView):
  template_name="hashez/fileSet.html"
  model=models.File

  def dispatch(self,request,*args,**kwargs):
    self.fileSetId=kwargs.get('pk');
    return super(FileSet,self).dispatch(request,*args,**kwargs)

  def get_queryset(self):
    return self.model.objects.filter(fileSet_id=self.fileSetId)

class BadFiles(ListView):
  template_name="hashez/badFiles.html"
  model=models.BadFiles

  def dispatch(self,request,*args,**kwargs):
    self.fileSetId=kwargs.get("pk")
    return super(BadFiles,self).dispatch(request,*args,**kwargs)

  def get_queryset(self):
    return self.model.objects.filter(fileSet_id=self.fileSetId)
