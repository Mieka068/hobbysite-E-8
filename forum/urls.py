from django.urls import path
from .views import PostListView, PostDetailView


urlpatterns = [
    path('threads/', PostListView.as_view(), name='forum_list'),
    path('thread/<int:pk>/', PostDetailView.as_view(), name='forum_thread'),
]

app_name = "forum"
