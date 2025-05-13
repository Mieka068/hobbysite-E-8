from django.contrib import admin
from .models import Thread, ThreadCategory


class ThreadCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name',)


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_on', 'updated_on')
    search_fields = ('title', 'entry', 'category__name')
    list_filter = ('category', 'created_on')
    ordering = ('-created_on',)  

admin.site.register(ThreadCategory, ThreadCategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
