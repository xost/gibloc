from django import template
from licenses import models

register=template.Library()

@register.inclusion_tag('licenses/navigation.html')
def navigation(group):
  return {'links':getattr(models,group).objects.all().order_by('item'),'group':group}
