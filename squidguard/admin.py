from django.contrib import admin
from models import Site, SiteACLs, Host, HostACLs

class SiteAdmin(admin.ModelAdmin):
  list_display=('item','descr',)
  search_fields=('item',)
  ordering=('item',)

class SiteACLsAdmin(admin.ModelAdmin):
  list_display=('item','descr',)
  search_fields=('item',)
  ordering=('item',)
  filter_horizontal=('Site',)

class HostAdmin(admin.ModelAdmin):
  list_display=('item','descr',)
  search_fields=('item',)
  ordering=('item',)

class HostACLsAdmin(admin.ModelAdmin):
  list_display=('item','descr',)
  search_fields=('item',)
  ordering=('item',)
  filter_horizontal=('Host','SiteACLs_deny','SiteACLs_allow',)

admin.site.register(Site,SiteAdmin)
admin.site.register(SiteACLs,SiteACLsAdmin)
admin.site.register(Host,HostAdmin)
admin.site.register(HostACLs,HostACLsAdmin)
