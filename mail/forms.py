# -*- coding: utf-8 -*-

import django.forms
import django.db
import models

class User(django.forms.ModelForm):
  passwd=django.forms.CharField(widget=django.forms.PasswordInput(),label=u'Пароль')
  email=django.forms.CharField(widget=django.forms.EmailInput(),label=u'email')
  class Meta():
    model=models.User
    fields='__all__'

class Alias(django.forms.ModelForm):
  src=django.forms.CharField(widget=django.forms.EmailInput())
  class Meta():
    model=models.Alias
    fields='__all__'

class Domain(django.forms.ModelForm):
  class Meta():
    model=models.Domain
    fields='__all__'

class Filter(django.forms.Form):
  fltr=django.forms.CharField(required=False,label=u'Фильтр')
