# -*- coding: utf8 -*-

import django.forms
import gibloc.settings
import models

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

