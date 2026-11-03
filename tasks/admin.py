from django.contrib import admin
from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'status', 'priority', 'due_date')
    search_fields = ('title', 'description')
    list_filter = ('status', 'priority', 'category')
