from django.contrib import admin
from models import Host,HostACLs,Port,PortACLs,Url,UrlACLs

class HostAdmin(admin.ModelAdmin):
  list_display=('item','descr',)
  search_fields=('item',)
  ordering=('item',)

class HostACLsAdmin(admin.ModelAdmin):
  list_display=('name','descr',)
  search_fields=('name',)
  ordering=('name',)

class PortAdmin(admin.ModelAdmin):
  list_display=('item','descr',)
  search_fields=('item',)
  ordering=('item',)

class PortACLsAdmin(admin.ModelAdmin):
  list_display=('name','descr',)
  search_fields=('name',)
  ordering=('name',)

class UrlAdmin(admin.ModelAdmin):
  list_display=('item','descr',)
  search_fields=('item',)
  ordering=('item',)

class UrlACLsAdmin(admin.ModelAdmin):
  list_display=('name','descr',)
  search_fields=('name',)
  ordering=('name',)

admin.site.register(Host,HostAdmin)
admin.site.register(HostACLs,HostACLsAdmin)
admin.site.register(Port,PortAdmin)
admin.site.register(PortACLs,PortACLsAdmin)
admin.site.register(Url,UrlAdmin)
admin.site.register(UrlACLs,UrlACLsAdmin)
