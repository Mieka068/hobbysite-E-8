from django.contrib import admin
from django.urls import path, include
from user_management import views as user_management_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', user_management_views.homepage, name='home'),
    path("user_management/", include("user_management.urls")),
    path("commissions/", include("commissions.urls")),
    path('blog/', include('blog.urls', namespace="blog")),
    path('wiki/', include('wiki.urls', namespace='wiki')),
    path('merchstore/', include('merchstore.urls')),
    path('forum/', include('forum.urls', namespace="forum")),
]
