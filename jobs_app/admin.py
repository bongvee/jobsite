from django.contrib import admin
from .models import Job

# ADDED to display columns
class JobTable(admin.ModelAdmin):
    list_display = ('title', 'company', 'lastDate')
    search_fields = ('title',)

admin.site.register(Job, JobTable)
