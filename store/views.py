from django.shortcuts import get_object_or_404, redirect, render
from .models import ProductType, Product

def list_view_redirect(request):
    return redirect('list_view')

def list_view(request):
    all_products = ProductType.objects.all()
    return render(request, 'list.html', {'all_products': all_products})

def detail_view(request, product_id): #(request, id_):
    product = get_object_or_404(id=product_id)
    return render(request, 'detail.html', {'product': product})