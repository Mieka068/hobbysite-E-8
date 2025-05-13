from django.contrib import admin
from .models import ArticleCategory, Article, Comment


class ArticleInline(admin.TabularInline):
    model = Article


class CommentInline(admin.TabularInline):
    model = Comment


class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    inlines = [ArticleInline]

    search_fields = ('name',)
    list_display = ('name',)


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    inlines = [CommentInline]

    search_fields = ('title',)
    list_display = ('title', 'created_on',)
    list_filter = ('category',)


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
