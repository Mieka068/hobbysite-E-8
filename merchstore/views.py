from django.http import HttpResponseForbidden
from .models import Profile
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .models import ProductType, Product
from .forms import AddProductForm, TransactionForm

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
    print("\nviews.py -> detail_view")
    print("Product Owner:", product.owner)
    print("Current User:", request.user)
    print("Comparison:", product.owner == request.user)
    return render(request, 'detail.html', {'product': product})

@login_required
def add_product_view(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, user=request.user)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user.profile
            product.save()
            return redirect('store:list_view')
    else:
        form = AddProductForm(user=request.user)

    return render(request, 'add_product.html', {'form': form})

@login_required
def buy_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check for invalid transaction attempts (e.g., buying own product, out of stock)
    if product.owner == request.user.profile:
        return HttpResponseForbidden("This is your product. Cannot do transaction.")
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user, product=product)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount <= product.stock:
                product.stock -= 1
                product.save()
                return redirect('store:list_view')
            else:
                form.add_error('amount', 'You have selected quantity higher than the available stock.')
    else:
        form = TransactionForm(user=request.user, product=product)

    return render(request, 'buy_product.html', {
        'form': form, 'product': product})