from django.contrib import admin
from . import models

# Register your models here.

class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',),}

admin.site.register(models.Department,DepartmentAdmin)
