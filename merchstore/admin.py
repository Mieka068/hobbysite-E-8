from django.contrib import admin
from merchstore import models
from .models import ProductType, Product, Transaction

class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    list_display = ['name', 'description']

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['name', 'product_type', 
                    'description', 'price'
                    ]

class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ['transaction_status', 'buyer', 
                    'product', 'amount',
                    'status', 'created_on'
                    ]
    
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)