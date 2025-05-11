from django.http import HttpResponseForbidden
from .models import Profile, Transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .models import ProductType, Product
from .forms import AddProductForm, TransactionForm, EditProductForm

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
    try:
        product_obj = Product.objects.get(id=product_id)
    
    except Product.DoesNotExist:
        return redirect('store:list_view')

    # Prevent invalid transaction attempts (e.g., buying own product, out of stock)
    if product_obj.owner == request.user.profile:
        return HttpResponseForbidden("This is your product. Cannot do transaction.")

    if request.method == 'POST':
        form = TransactionForm(data=request.POST, user=request.user, product=product_obj)
        
        if form.is_valid():
            amount = form.cleaned_data['amount']

            if amount <= product_obj.stock:
                transaction = form.save(commit=False)
                transaction.buyer = request.user.profile
                transaction.amount = amount
                transaction.save()
                product_obj.stock -= amount
                product_obj.save()
                return redirect('store:cart_view')
            else:
                form.add_error('amount', 'You have selected quantity higher than the available stock.')
    
    else:
        form = TransactionForm(user=request.user, product=product_obj)

    return render(request, 'buy_product.html', {
        'form': form, 'product': product_obj})

@login_required
def cart_view(request):
    user = request.user
    if user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            user_profile = None
         
        # Get all products the user has purchased
        purchases = Transaction.objects.filter(
            buyer=user_profile,
        ).select_related('product').order_by('product__name')
        
        print("Purchased Products:", purchases)  # Debugging Output
        ctx = {
            'purchases': purchases,
            'cart_size': purchases.count(),
        }
    else:
        ctx = {
            'all_products': Product.objects.all()
        }
    return render(request, 'cart.html', ctx)

@login_required
def edit_product_view(request, product_id):
    selected_product = get_object_or_404(Product, id=product_id)

    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        form = EditProductForm(request.POST, user=user_profile, instance=selected_product)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = user_profile
            product.save()
            return redirect('store:list_view')
    else:
        form = EditProductForm(user=user_profile, instance=selected_product)

    return render(request, 'edit_product.html', {
        'form': form,
        'user': user_profile,
        'product': selected_product
    })

def transactions_view(request):
    user = request.user
    if user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            user_profile = None
         
        transactions = Transaction.objects.exclude(
            buyer=user_profile
        ).exclude(
            product__isnull=True
        ).select_related('product').order_by('product__name')

        print("Products sold:", transactions)
        ctx = {
            'transactions': transactions,
            'transactions_made': transactions.count(),
        }
    else:
        ctx = {
            'all_products': Product.objects.all()
        }
    return render(request, 'transactions.html', ctx)
