from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleCreateView


urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
    path('article/add', ArticleCreateView.as_view(), name='article_create')
]

app_name = 'wiki'
