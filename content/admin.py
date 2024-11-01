from django.contrib import admin
from content.models import Content, Category


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'photo', 'publication_date', 'category', 'is_content_paid')


@admin.register(Category)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
