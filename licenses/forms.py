import django.forms
import django.db
import models

class License(django.forms.ModelForm):
  class Meta():
    model=models.License
    fields=['item','descr','group','owner']

class LicenseG(django.forms.ModelForm):
  class Meta():
    model=models.LicenseG
    fields=['item','descr']

class OwnerG(django.forms.ModelForm):
  class Meta():
    model=models.OwnerG
    fields=['item','descr']

class Owner(django.forms.ModelForm):
  class Meta():
    model=models.Owner
    fields=['item','descr','group']
