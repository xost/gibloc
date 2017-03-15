# -*- coding: utf8 -*-

from django import forms
import gibloc.settings

class ReportQueryForm(forms.Form):
  starttime=forms.DateField(input_formats=gibloc.settings.DATE_INPUT_FORMATS,label=u'Начало')
  deadtime=forms.DateField(input_formats=gibloc.settings.DATE_INPUT_FORMATS,label=u'Конец')
