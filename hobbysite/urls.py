from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("commissions/", include("commissions.urls")),
    path('blog/', include('blog.urls', namespace="blog")),
    path('wiki/', include('wiki.urls', namespace='wiki')),
    path('merchstore/', include('store.urls')),
    path('forum/', include('forum.urls', namespace="forum")),
    path("", include("user_management.urls")),
]
