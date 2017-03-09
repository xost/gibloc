from django import template
from hashez import models

register=template.Library()

@register.inclusion_tag('hashez/navigation.html')
def navigation():
  clients=models.File.objects.all()
  return {'clients':models.Client.objects.all()}
                            
