from django.contrib import admin
from categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'color', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
