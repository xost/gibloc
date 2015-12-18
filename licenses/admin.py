from django.contrib import admin
from models import OwnerG,LicenseG,Owner,License

class OwnerGAdmin(admin.ModelAdmin):
  list_display=('item','descr',)
  search_fields=('item',)
  ordering=('item',)

class LicenseGAdmin(admin.ModelAdmin):
  list_display=('item','descr',)
  search_fields=('item',)
  ordering=('item',)

class OwnerAdmin(admin.ModelAdmin):
  list_display=('item','descr',)
  search_fields=('item',)
  ordering=('item',)

class LicenseAdmin(admin.ModelAdmin):
  list_display=('item','descr',)
  search_fields=('item',)
  ordering=('item',)

admin.site.register(OwnerG,OwnerGAdmin)
admin.site.register(LicenseG,LicenseGAdmin)
admin.site.register(Owner,OwnerAdmin)
admin.site.register(License,LicenseAdmin)
