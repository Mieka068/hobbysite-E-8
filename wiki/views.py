from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import ArticleCategory


class ArticleListView(ListView):
    model = ArticleCategory
    template_name = 'wiki/list.html'
    context_object_name = 'categories'


class ArticleDetailView(DetailView):
    model = ArticleCategory
    template_name = 'wiki/detail.html'
    context_object_name = 'category'


def article_list(request):
    categories = ArticleCategory.objects.all()
    return render(request, 'wiki/list.html', {'categories': categories})

def article_detail(request, pk):
    category = get_object_or_404(ArticleCategory, pk=pk)
    return render(request, 'wiki/detail.html', {'category': category})
