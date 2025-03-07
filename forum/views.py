from django.shortcuts import render, get_object_or_404
from .models import Post, PostCategory

def forum_list(request):
    posts = Post.objects.all()
    return render(request, 'forum/forum_list.html', {'posts': posts})

def forum_thread(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'forum/forum_thread.html', {'post_id': post_id})

# Create your views here.