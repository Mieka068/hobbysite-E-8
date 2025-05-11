from urllib import request
from django import forms
from .models import Product, ProductType, Transaction, Profile

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'owner',
            'product_type', 'description',
            'price', 'stock',
            'status'
        ]
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.fields['owner'].initial = user.profile
        self.fields['owner'].disabled = True

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['buyer', 'product', 'amount']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        profile = Profile.objects.get(user=user)
        product = kwargs.pop('product', None)
        super(TransactionForm, self).__init__(*args, **kwargs)

        self.fields['buyer'] = forms.ModelChoiceField(
            queryset=Profile.objects.filter(id=profile.id),
            initial=profile,
        )

        self.fields['product'] = forms.ModelChoiceField(
            queryset=Product.objects.filter(id=product.id),
            initial=product,
        )

        self.fields['buyer'].disabled = True
        self.fields['product'].disabled = True
        self.fields['amount'].widget.attrs['max'] = product.stock
        self.fields['amount'].widget.attrs['min'] = 1
        self.fields['amount'].initial = 1

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'owner',
            'product_type', 'description',
            'price', 'stock',
            'status'
        ]
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditProductForm, self).__init__(*args, **kwargs)
        
        instance = self.instance
        self.fields['owner'].initial = user.display_name
        self.fields['owner'].disabled = True
        self.fields['name'].initial = instance.name
        self.fields['product_type'].initial = instance.product_type
        self.fields['description'].initial = instance.description
        self.fields['price'].initial = instance.price
        self.fields['stock'].initial = instance.stock
        self.fields['status'].initial = instance.status
    
