from django.forms import ModelForm
import models

class Host(ModelForm):
  class Meta():
    model=models.Host
    fields=('item','descr')

class Site(ModelForm):
  class Meta():
    model=models.Site
    fields='__all__'
