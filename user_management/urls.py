from django.urls import path
<<<<<<< HEAD
from . import views
=======
from .views import profile_update
<<<<<<< HEAD
>>>>>>> 566bcc5 (Merged 'store' with user_management.)
=======
from . import views
>>>>>>> 0d99399 (Applied homepage.)

app_name = "user_management"

urlpatterns = [
<<<<<<< HEAD
    #keep in Profile App
    path('', views.homepage, name='homepage'),
    
    #keep in Profile App
    path('profile/', views.profile_update, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'), 
]
=======
    path("profile", profile_update, name="profile"),
<<<<<<< HEAD
]
>>>>>>> 566bcc5 (Merged 'store' with user_management.)
=======
    path('', views.homepage, name='homepage'),

]
>>>>>>> 0d99399 (Applied homepage.)
