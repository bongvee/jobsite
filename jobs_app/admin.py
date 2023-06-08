from django.contrib import admin
from .models import Job

# ADDED to display columns
# class JobsTable(admin.ModelAdmin):
#     list_display = ('title', 'company', '-lastDate')
#     search_fields = ('task_title',)

admin.site.register(Job)
