import models
import django.forms
from django.forms.extras.widgets import SelectDateWidget

class TaskG(django.forms.ModelForm):
  class Meta():
    model=models.TaskG
    fields='__all__'

class Task(django.forms.ModelForm):
  starttime=django.forms.DateField(widget=SelectDateWidget(),required=False)
  deadtime=django.forms.DateField(widget=SelectDateWidget(),required=False)
  class Meta():
    model=models.Task
    exclude=('addtime','owner','group')

class Comment(django.forms.ModelForm):
  class Meta():
    model=models.Comment
    exclude=('addtime','owner','task')
