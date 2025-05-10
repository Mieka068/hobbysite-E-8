from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("commissions/", include("commissions.urls")),
    path('blog/', include('blog.urls', namespace="blog")),
    path('wiki/', include('wiki.urls', namespace='wiki')),
    path('merchstore/', include('store.urls')),
    path('forum/', include('forum.urls', namespace="forum")),
    path("", TemplateView.as_view(template_name="user_management/homepage.html"), name="home"),
    path("usermanagement/", include("user_management.urls", namespace="user_management")),
    path('accounts/', include('django.contrib.auth.urls'))
]
