from django.contrib import admin

from .models import ArticleCategory, Article

class ArticleInline(admin.TabularInline):
    model = Article

    search_fields = ('name', 'category', 'created_on', 'entry', )

class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    inlines = [ArticleInline]

    search_fields = ('name', )

    ('Details', {
        'ingredients':
            ('name', 'quantity')
    })

class ArticleAdmin(admin.ModelAdmin):
    model=Article
    fieldsets = [
        ('Details', {
            'fields': [
                ('name', 'entry'), 'articlecategory'
            ]
        }),
    ]

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
