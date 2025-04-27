from django.http import HttpResponseRedirect
from django.urls import include, path

from merchstore import views
<<<<<<< HEAD

app_name = 'merchstore'
=======
>>>>>>> 8d2415d (Renamed app from store to merchstore and made changes to relevant files.)

app_name = 'merchstore'

urlpatterns = [
<<<<<<< HEAD
    path('items/', views.list_view, name='list_view'),
    path('item/<int:product_id>/', views.detail_view, name='detail_view'),
=======
    path('', views.list_view_redirect, name='list_view_redirect'),
    path('items/', views.list_view, name='list_view'),
    path('merchstore/item/<int:product_id>/', views.detail_view, name='detail_view'),
>>>>>>> 9b61377 (Fixed views.)
]