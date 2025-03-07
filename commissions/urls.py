from django.urls import path
from commissions import views


app_name = "commissions"

urlpatterns = [
    path("list/", views.CommissionListView.as_view(), name="list"),
    path("detail/<int:pk>/", views.CommissionDetailView.as_view(), name="detail"),
]

