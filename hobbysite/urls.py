from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', user_management_views.homepage, name='home'),
    path("user_management/", include("user_management.urls")),
    path("commissions/", include("commissions.urls")),
    path('blog/', include('blog.urls', namespace="blog")),
    path('wiki/', include('wiki.urls', namespace='wiki')),
    path('merchstore/', include('merchstore.urls')),
    path('forum/', include('forum.urls', namespace="forum")),
    path("", TemplateView.as_view(template_name="user_management/homepage.html"), name="home"),
    path("usermanagement/", include("user_management.urls", namespace="user_management")),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
