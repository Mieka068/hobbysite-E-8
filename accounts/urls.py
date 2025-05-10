from django.urls import path
from user_management.views import login_view, logout_view, register_view
from django.contrib.auth import views as auth_views 


app_name = "accounts"

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),  
    path('reset/confirm', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  
]