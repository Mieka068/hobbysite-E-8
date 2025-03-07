from django.contrib import admin
from .models import Post, PostCategory

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_on', 'updated_on')
    search_fields = ('title', 'entry', 'category__name')
    list_filter = ('category', 'created_on')
    ordering = ('-created_on',)  

admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostAdmin)
# Register your models here.
