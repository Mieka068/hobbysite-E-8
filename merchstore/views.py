from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .models import ProductType, Product
from .forms import AddProductForm

def list_view(request):
    all_products = Product.objects.all()
    return render(request, 'list.html', {'all_products': all_products})

def detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'detail.html', {'product': product})

@login_required
def add_product_view(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:list_view')
    else:
        form = AddProductForm()

    return render(request, 'add_product.html', {'form': form})