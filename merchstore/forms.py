from django import forms
from .models import Product, ProductType, Transaction

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
        self.fields['owner'].initial = user
        self.fields['owner'].disabled = True

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['status', 'buyer', 
                  'product', 'amount', 
                  'status'
                  ]
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        product = kwargs.pop('product', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['buyer'].initial = user
        self.fields['buyer'].disabled = True
        self.fields['amount'].widget.attrs['max'] = product.stock
        self.fields['amount'].widget.attrs['min'] = 1
        self.fields['amount'].initial = 1  # Default value
