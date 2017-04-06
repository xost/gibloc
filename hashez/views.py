# -*- coding: utf8 -*-

from django.shortcuts import render
from django.views.generic import ListView,TemplateView,DetailView
from gibloc.mixins import LoginRequiredMixin
import datetime
import models,forms,gibloc

class Simple(LoginRequiredMixin,TemplateView):
  template_name="hashez/simple.html"

class Events(LoginRequiredMixin):
  sqlQuery=""" SELECT E.id,
                      E.eventType,
                      E.result,
                      E.registred,
                      E.fileSet_id,
                      (
                        SELECT count(*)
                        FROM hashez_file F
                        WHERE F.fileSet_id=E.fileSet_id
                      ) as files_count,
                      (
                        SELECT count(*)
                        FROM hashez_badfiles B
                        WHERE B.event_id=E.id
                      ) as badFiles_event_id
               FROM hashez_event E
               WHERE E.client_id={0} {1}
               ORDER BY E.id {2}
           """
  dateFilter="AND (CAST(E.registred AS DATE) BETWEEN '{0}' AND '{1}')"

class EventList(ListView,Events):
  template_name='hashez/events.html'
  form=forms.ReportQueryForm
  err={}

  def dispatch(self,request,*args,**kwargs):
    self.clientId=kwargs.get('pk')
    return super(EventList,self).dispatch(request,*args,**kwargs)

  def get(self,request,*args,**kwargs):
    self.sort=request.GET.get('sort');
    try:
      self.fromDate=datetime.datetime.strptime(request.GET.get('fromDate'),'%d/%m/%Y').date() if request.GET.get('fromDate') else ''
      self.toDate=datetime.datetime.strptime(request.GET.get('toDate'),'%d/%m/%Y').date() if request.GET.get('toDate') else ''
      print self.fromDate
      print self.toDate
    except ValueError,e:
      self.err['toDate']=('Неверный формат даты')
      raise ValueError(e)
    return super(EventList,self).get(request,*args,**kwargs)
  
  def get_queryset(self):
    if(self.fromDate and self.toDate):
      self.dateFilter=self.dateFilter.format(self.fromDate,self.toDate)
    else:
      self.dateFilter=''
    sqlQuery=self.sqlQuery.format(self.clientId,
                                  self.dateFilter,
                                  "DESC" if self.sort=="DESC" else "ASC");
    qset=models.Event.objects.raw(sqlQuery)
    return qset

  def get_context_data(self,**kwargs):
    kwargs['form']=self.form
    kwargs['fromDate']=str(self.fromDate)
    kwargs['toDate']=str(self.toDate)
    kwargs['clientId']=self.clientId
    return super(EventList,self).get_context_data(**kwargs)

class ClientDetail(LoginRequiredMixin,DetailView):
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

class FileSet(LoginRequiredMixin,ListView):
  template_name="hashez/fileSet.html"
  model=models.File

  def dispatch(self,request,*args,**kwargs):
    self.fileSetId=kwargs.get('pk');
    return super(FileSet,self).dispatch(request,*args,**kwargs)

  def get_queryset(self):
    return self.model.objects.filter(fileSet_id=self.fileSetId)

class BadFiles(LoginRequiredMixin,ListView):
  template_name="hashez/badFiles.html"
  model=models.BadFiles

  def dispatch(self,request,*args,**kwargs):
    self.eventId=kwargs.get("pk")
    return super(BadFiles,self).dispatch(request,*args,**kwargs)

  def get_queryset(self):
    return self.model.objects.filter(event_id=self.eventId)

class Report(ListView,Events):
  template_name="hashez/report.html"

  def get(self,request,*args,**kwargs):
    self.clientId=request.GET.get("clientId")
    self.fromDate=request.GET.get("fromDate")
    self.toDate=request.GET.get("toDate")
    return super(Report,self).get(request,*args,**kwargs)

  def get_queryset(self):
    self.dateFilter=self.dateFilter.format(self.fromDate,self.toDate)
    sqlQuery=self.sqlQuery.format(self.clientId,
                                  self.dateFilter,
                                  "ASC",
                                 )
    qset=models.Event.objects.raw(sqlQuery)
    return qset

  def get_context_data(self,**kwargs):
    kwargs['clientId']=self.clientId
    kwargs['fromDate']=self.fromDate
    kwargs['toDate']=self.toDate
    kwargs['client']=models.Client.objects.get(pk=self.clientId)
    return super(Report,self).get_context_data(**kwargs)
