from django.db import models
from django.urls import reverse


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField

    class Meta:
        ordering = ['name']
        unique_together = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category'
        )
    entry = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('blog:article', args=[str(self.pk)])

    class Meta:
        ordering = ['-created_on']
        unique_together = ['title']
        verbose_name = 'article'
        verbose_name_plural = 'articles'
