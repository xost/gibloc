from models import Host,Port,Url
from django.forms import ModelForm
from django import forms

class HostForm(ModelForm):
  class Meta():
    model=Host
    fields=('item','descr')

class PortForm(ModelForm):
  class Meta():
    model=Port
    fields='__all__'

class UrlForm(ModelForm):
  class Meta():
    model=Url
    fields='__all__'
