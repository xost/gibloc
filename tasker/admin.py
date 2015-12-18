from django.contrib import admin
from models import Task,TaskG

class TaskAdmin(admin.ModelAdmin):
  list_display=('name','description',)
  search_fields=('name',)
  ordering=('name',)

class TaskGAdmin(admin.ModelAdmin):
  list_display=('name','description',)
  search_fields=('name',)
  ordering=('name',)


#class StateAdmin(admin.ModelAdmin):
#  list_display=('state','description',)
#  search_fields=('state',)
#  ordering=('state',)
#
#class PersonAdmin(admin.ModelAdmin):
#  list_display=('name','description',)
#  search_fields=('name',)
#  ordering=('name',)

admin.site.register(Task,TaskAdmin)
admin.site.register(TaskG,TaskGAdmin)
#admin.site.register(State,StateAdmin)
#admin.site.register(Person,PersonAdmin)
