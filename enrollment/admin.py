from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Enrollment)
admin.site.register(models.CourseResult)