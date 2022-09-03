from django.contrib import admin
from .models import *


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'photo', 'category', 'created_at', 'update_at', 'is_publish','views')
    list_display_links = ('id', 'title', 'category')
    search_fields = ('id', 'title')
    list_editable = ('is_publish',)
    list_filter = ('is_publish', 'category')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
