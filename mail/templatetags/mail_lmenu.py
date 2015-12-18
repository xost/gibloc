from django import template
from mail import models

register=template.Library()

@register.inclusion_tag('mail/navigation.html')
def navigation(model):
  return{'links':getattr(models,model).objects.all(),'model':model}
