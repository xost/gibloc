# -*- coding: utf8 -*-

import django.forms
import models
import gibloc.settings

class Cert(django.forms.ModelForm):
  starttime=django.forms.DateField(input_formats=gibloc.settings.DATE_INPUT_FORMATS,label=u'Начало действия')
  deadtime=django.forms.DateField(input_formats=gibloc.settings.DATE_INPUT_FORMATS,label=u'Конец действия')
  class Meta:
    model=models.Cert
    exclude=('addedby',)

class Group(django.forms.ModelForm):
  class Meta:
    model=models.Group
    fields='__all__'

class Owner(django.forms.ModelForm):
  class Meta:
    model=models.Owner
    fields='__all__'

class Issuer(django.forms.ModelForm):
  class Meta:
    model=models.Issuer
    fields='__all__'

class Skzi(django.forms.ModelForm):
  class Meta:
    model=models.Skzi
    fields='__all__'

class Type(django.forms.ModelForm):
  class Meta:
    model=models.Type
    fields='__all__'

class Area(django.forms.ModelForm):
  class Meta:
    model=models.Area
    fields='__all__'

class LMenuForm(django.forms.Form):
  groups=django.forms.ModelMultipleChoiceField(label="Группа",queryset=models.Group.objects.all(),
    widget=django.forms.CheckboxSelectMultiple)
  owner=django.forms.ModelMultipleChoiceField(label="Сотрудник",queryset=models.Owner.objects.all(),
    widget=django.forms.CheckboxSelectMultiple)
  issuer=django.forms.ModelMultipleChoiceField(label="Издатель",queryset=models.Issuer.objects.all(),
    widget=django.forms.CheckboxSelectMultiple)
  skzi=django.forms.ModelMultipleChoiceField(label="СКЗИ",queryset=models.Skzi.objects.all(),
    widget=django.forms.CheckboxSelectMultiple)
  type=django.forms.ModelMultipleChoiceField(label="Вид ключевой информации",queryset=models.Type.objects.all(),
    widget=django.forms.CheckboxSelectMultiple)
  area=django.forms.ModelMultipleChoiceField(label="Область действия",queryset=models.Area.objects.all(),
    widget=django.forms.CheckboxSelectMultiple)
  reverse=django.forms.BooleanField(label="Реверс")
