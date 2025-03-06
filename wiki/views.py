from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import ArticleCategory


class ArticleListView(ListView):
    model = ArticleCategory
    template_name = 'wiki/list.html'


class ArticleDetailView(DetailView):
    model = ArticleCategory
    template_name = 'wiki/list.html'
