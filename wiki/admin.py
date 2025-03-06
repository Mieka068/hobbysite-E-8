from django.contrib import admin
from .models import ArticleCategory, Article


class ArticleInline(admin.TabularInline):
    model = Article


class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    inlines = [ArticleInline]

    search_fields = ('name',)
    list_display = ('name',)


class ArticleAdmin(admin.ModelAdmin):
    model = Article

    search_fields = ('title',)
    list_display = ('title', 'created_on',)
    list_filter = ('category',)


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
