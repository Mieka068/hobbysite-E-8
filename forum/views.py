from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Thread, ThreadCategory, Comment
from .forms import CommentForm


class ThreadListView(ListView):
    model = Thread
    template_name = 'forum/thread_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return ThreadCategory.objects.prefetch_related('threads')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_threads'] = Thread.objects.filter(author=self.request.user)
            context['other_threads'] = Thread.objects.exclude(author=self.request.user)
        else:
            context['user_threads'] = []
            context['other_threads'] = Thread.objects.all()
        return context


class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'forum/thread_detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = self.get_object()
        context['comments'] = thread.comments.all()
        context['related_threads'] = Thread.objects.filter(
            category=thread.category
        ).exclude(pk=thread.pk)[:2]
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.thread = self.object
                comment.save()
                return redirect('forum:thread_detail', pk=self.object.pk)
        return self.get(request, *args, **kwargs)


class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    fields = ['title', 'category', 'entry']
    template_name = 'forum/thread_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ThreadUpdateView(LoginRequiredMixin, UpdateView):
    model = Thread
    fields = ['title', 'category', 'entry']
    template_name = 'forum/thread_form.html'
