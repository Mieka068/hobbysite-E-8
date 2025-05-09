from .models import Profile
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .models import ProductType, Product
from .forms import AddProductForm

def list_view(request):
    user = request.user
    if user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            user_profile = None
        
        owned_products = Product.objects.filter(owner=user_profile)
        other_products = Product.objects.exclude(owner=user_profile)
        ctx = {
            'owned_products': owned_products,
            'other_products': other_products,
        }
    else:
        ctx = {
            'all_products': Product.objects.all()
        }
    return render(request, 'list.html', ctx)

def detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'detail.html', {'product': product})

@login_required
def add_product_view(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user.profile
            product.save()
            return redirect('store:list_view')
    else:
        form = AddProductForm()

    return render(request, 'add_product.html', {'form': form})