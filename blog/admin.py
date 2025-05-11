from django.contrib import admin
from .models import ArticleCategory, Article


class ArticleInline(admin.TabularInline):
    model = Article

    search_fields = ('title', 'category', 'created_on', 'entry', )


class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    inlines = [ArticleInline]

    search_fields = ('name', )


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ('title', 'created_on',)
    list_filter = ('category',)

    fieldsets = [
        ('Details', {
            'fields': [
                'title',
                'entry',
                'category',
                'header_img'
            ]
        }),
    ]


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
