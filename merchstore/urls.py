from django.http import HttpResponseRedirect
from django.urls import include, path

from merchstore import views

app_name = 'merchstore'

app_name = 'store'

urlpatterns = [
    path('items/', views.list_view, name='list_view'),
    path('item/<int:product_id>/', views.detail_view, name='detail_view'),
]