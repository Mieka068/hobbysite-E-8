from django.contrib import admin
from merchstore import models
from .models import ProductType, Product

class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    list_display = ['name', 'description']

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['name', 'product_type', 'description', 'price']

admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
