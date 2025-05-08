from django.shortcuts import get_object_or_404, redirect, render
from .models import ProductType, Product

def list_view(request):
    all_products = Product.objects.all()
    return render(request, 'list.html', {'all_products': all_products})

def detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'detail.html', {'product': product})