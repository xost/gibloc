from django.contrib import admin
import models

class DomainAdmin(admin.ModelAdmin):
  display_list=('name','descr',)

class UserAdmin(admin.ModelAdmin):
  display_list=('email','descr',)

class AliasAdmin(admin.ModelAdmin):
  display_list=('src','dst','descr',)

admin.site.register(models.Domain,DomainAdmin)
admin.site.register(models.User,UserAdmin)
admin.site.register(models.Alias,AliasAdmin)
