from django.urls import path
from .views import profile_update
from . import views

app_name = "user_management"

urlpatterns = [
    path("profile", profile_update, name="profile"),
    path('', views.homepage, name='homepage'),

]