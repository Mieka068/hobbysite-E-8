from django.http import HttpResponseRedirect
from django.urls import include, path

from store import views

urlpatterns = [
    path('', views.list_view_redirect, name='list_view_redirect'),
    path('merchstore/items', views.list_view, name = 'list_view'),
    path('merchstore/item', views.detail_view, name = 'detail_view'),
    # path('merchstore/items/<int:id>/', views.detail_view, name = 'detail_view'),
]