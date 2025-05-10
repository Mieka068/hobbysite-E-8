from django.urls import path
from . import views

app_name = "user_management"

urlpatterns = [
    #keep in Profile App
    path('', views.homepage, name='homepage'),
    
    #keep in Profile App
    path('profile/', views.profile_update, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'), 
]