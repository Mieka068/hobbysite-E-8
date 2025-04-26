from django.http import HttpResponseRedirect
from django.urls import include, path

from merchstore import views
<<<<<<< HEAD

app_name = 'merchstore'
=======
>>>>>>> 8d2415d (Renamed app from store to merchstore and made changes to relevant files.)

app_name = 'merchstore'

urlpatterns = [
    path('items/', views.list_view, name='list_view'),
    path('item/<int:product_id>/', views.detail_view, name='detail_view'),
]