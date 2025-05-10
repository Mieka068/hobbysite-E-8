from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ArticleCategory, Article
from .forms import ArticleForm, CommentForm


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'blog/article_list.html'
    
    def get_queryset(self):
        user_articles = Article.objects.filter(author=self.request.user)
        all_articles = Article.objects.exclude(author=self.request.user)
        return all_articles, user_articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_articles, my_articles = self.get_queryset()
        
        category_groups = {}
        for category in ArticleCategory.objects.all():
            category_groups[category] = all_articles.filter(category=category)

        context['category_groups'] = category_groups
        context['my_articles'] = my_articles
        context['categories'] = ArticleCategory.objects.all() 

        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()

        context['article_author'] = article.author
        context['other_articles'] = Article.objects.filter(
            author=article.author).exclude(id=article.id)[:2]  # Get at least 2 other articles

        context['comments'] = article.comments.all().order_by('-created_on')

        context['comment_form'] = CommentForm()

        return context

    def post(self, request, *args, **kwargs):
        article = self.get_object()

        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.article = article
                comment.author = request.user.profile 
                comment.save()

                return redirect('blog:article', pk=article.pk)

        return self.get(request, *args, **kwargs)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = '__all__'
    form_class = ArticleForm


    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = '__all__'
    template_name = 'artice_detail.html'
    form_class = ArticleForm
    success_url = reverse_lazy('blog:article_list')
    
