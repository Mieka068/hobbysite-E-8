from django.urls import path
from . import views

urlpatterns = [
    path('threads/', views.forum_list, name='forum_list'),
    path('thread/<int:post_id>/', views.forum_thread, name='forum_thread'),
]

app_name = "forum"