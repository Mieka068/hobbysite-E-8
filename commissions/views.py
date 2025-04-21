from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Commission


class CommissionListView(ListView):
    model = Commission
    template_name = "commissions/list.html"
    context_object_name = "commissions"


class CommissionDetailView(DetailView):
    model = Commission
    template_name = "commissions/detail.html"
    context_object_name = "commission"