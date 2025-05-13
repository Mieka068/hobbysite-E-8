from django.http import HttpResponseRedirect
from django.urls import include, path

from merchstore import views

app_name = 'merchstore'

urlpatterns = [
    path('', views.list_view, name='list_view'),
    path('items/', views.list_view, name='list_view'),
    path('cart/', views.cart_view, name='cart_view'),
    path('items/item/<int:product_id>/', views.detail_view, name='detail_view'),
    path('item/add/', views.add_product_view, name='add_product_view'),
    path('items/item/<int:product_id>/buy/', views.buy_product_view, name='buy_product_view'),
    path('items/item/<int:product_id>/edit/', views.edit_product_view, name='edit_product_view'),
    path('transactions/', views.transactions_view, name='transactions_view')
    ]