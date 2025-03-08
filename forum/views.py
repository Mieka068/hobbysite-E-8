from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, PostCategory


class PostListView(ListView):
    model = PostCategory
    template_name = 'forum/forum_list.html'
    context_object_name = 'categories'


class PostDetailView(DetailView):
    model = PostCategory
    template_name = 'forum/forum_thread.html'
    context_object_name = 'category'


def forum_list(request):
    categories = PostCategory.objects.all()
    return render(request, 'forum/forum_list.html', {'categories': categories})

def forum_thread(request, pk):
    category = get_object_or_404(PostCategory, pk=pk)
    return render(request, 'forum/forum_thread.html', {'category': category})

# Create your views here.