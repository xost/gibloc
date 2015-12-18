# -*- coding: utf8 -*-

from django.contrib import admin
from models import Group,Owner,Issuer,Skzi,Area,Type

class GroupAdmin(admin.ModelAdmin):
  search_fields=('item',)
  ordering=('item',)

class OwnerAdmin(admin.ModelAdmin):
  search_fields=('item',)
  ordering=('item',)

class SkziAdmin(admin.ModelAdmin):
  search_fields=('item',)
  ordering=('item',)

class IssuerAdmin(admin.ModelAdmin):
  search_fields=('item',)
  ordering=('item',)

class AreaAdmin(admin.ModelAdmin):
  search_fields=('item',)
  ordering=('item',)

class TypeAdmin(admin.ModelAdmin):
  search_fields=('item',)
  ordering=('item',)

admin.site.register(Group,GroupAdmin)
admin.site.register(Owner,OwnerAdmin)
admin.site.register(Issuer,IssuerAdmin)
admin.site.register(Skzi,SkziAdmin)
admin.site.register(Type,TypeAdmin)
admin.site.register(Area,AreaAdmin)
