from django import forms
from .models import Product, ProductType, Transaction

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'product_type',
            'description', 'price',
            'stock', 'status'
        ]