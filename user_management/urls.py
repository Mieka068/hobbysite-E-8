from django.urls import path
from . import views

app_name = "user_management"

urlpatterns = [
    #keep in Profile App
    path('', views.homepage, name='homepage'),

    # transfer to Accounts app
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    #keep in Profile App
    path('profile/', views.profile_update, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'), 
]
