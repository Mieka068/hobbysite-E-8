from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import ArticleCategory, Article


class ArticleListView(ListView):
    model = ArticleCategory
    template_name = 'wiki/list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['user_articles'] = Article.objects.filter(poster=user)
        return context


class ArticleDetailView(DetailView):
    model = ArticleCategory
    template_name = 'wiki/detail.html'
    context_object_name = 'category'
