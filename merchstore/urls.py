from django.http import HttpResponseRedirect
from django.urls import include, path

from merchstore import views

app_name = 'merchstore'

urlpatterns = [
    path('', views.list_view_redirect, name='list_view_redirect'),
    path('items/', views.list_view, name='list_view'),
    path('merchstore/item/<int:product_id>/', views.detail_view, name='detail_view'),
]