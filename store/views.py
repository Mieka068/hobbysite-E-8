from django.shortcuts import redirect, render
# from .models import ProductType, Product

def list_view_redirect(request):
    return redirect('list_view')

def list_view(request):
    # all_products = ProductType.objects.all()
    return render(request, 'list.html')

def detail_view(request): #(request, id_):
    # products = Product.objects.get(id=id_)
    return render(request, 'detail.html')