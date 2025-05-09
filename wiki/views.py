from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import ArticleCategory, Article, Comment
from user_management.models import Profile
from .forms import ArticleForm, CommentForm


class ArticleListView(ListView):
    model = ArticleCategory
    template_name = 'wiki/list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            profile = get_object_or_404(Profile, user=user)
            context['user_articles'] = Article.objects.filter(author=profile)
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
        context['other_articles'] = []
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'wiki/create_update.html'
    form_class = ArticleForm
    success_url = reverse_lazy('wiki:article_list')

    def form_valid(self, form):
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)
        form.instance.author = profile
        response = super().form_valid(form)
        return response


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'wiki/create_update.html'
    form_class = ArticleForm
    success_url = reverse_lazy('wiki:article_list')
