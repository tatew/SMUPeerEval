from django.contrib import admin

from .models import Course, Professor
# Register your models here.
admin.site.register(Course)
admin.site.register(Professor)