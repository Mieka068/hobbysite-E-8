from django.db import models
from django.urls import reverse
from user_management.models import Profile


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
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name='author'
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles'
        )
    entry = models.TextField(null=True)
    header_img = models.ImageField(upload_to='headers/')
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


class Comment(models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name='author'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_on']
        verbose_name = 'comment'
        verbose_name_plural = 'comments'



