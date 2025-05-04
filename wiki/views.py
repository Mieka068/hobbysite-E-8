from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import ArticleCategory, Article, Comment
from .forms import ArticleForm, CommentForm


class ArticleListView(ListView):
    model = ArticleCategory
    template_name = 'wiki/list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['user_articles'] = Article.objects.filter(author=user)
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'wiki/detail.html'
    context_object_name = 'article'
    form_class = CommentForm
    success_url = reverse_lazy('wiki:article_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object
        user = self.request.user
        if user.is_authenticated:
            profile = get_object_or_404(Profile, user=user)
            context['is_author'] = article.author == user
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'wiki/create_update.html'
    form_class = ArticleForm
    success_url = reverse_lazy('wiki:article_list')


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'wiki/create_update.html'
    form_class = ArticleForm
    success_url = reverse_lazy('wiki:article_list')
