from django.urls import path
from commissions import views
from .views import (
    CommissionListView, CommissionDetailView,
    CommissionCreateView, CommissionUpdateView
)


app_name = "commissions"


urlpatterns = [
    path("list/", views.CommissionListView.as_view(), name="list"),
    path("detail/<int:pk>/", views.CommissionDetailView.as_view(), name="detail"),
    path('<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),
    path('application/<int:application_id>/accept/', views.accept_application, name='accept_application'),
    path('application/<int:application_id>/reject/', views.reject_application, name='reject_application'),
    path('job/<int:job_id>/applications/', views.job_applications_view, name='job_applications'),
    path("add/", CommissionCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", CommissionUpdateView.as_view(), name="update"),
]

