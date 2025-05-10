from django.db import models
from django.urls import reverse

from user_management.models import Profile

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
    
class Product(models.Model):
    status_options = [
        ('Available', 'Available'),
        ('On sale', 'On sale'),
        ('Out of stock', 'Out of stock')
        ]
    
    name = models.CharField(max_length=255)

    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null = True,
        related_name = 'products_of_type'
    )

    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='products_of_owner'
    )
    
    description = models.TextField()

    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )

    stock = models.PositiveIntegerField()

    status = models.CharField(
        max_length = 20,
        choices = status_options,
        default = 'Available'
    )

    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.status = 'Out of stock'

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('store:detail_view', args=[str(self.id)])

    class Meta:
        ordering = ['name']

class Transaction(models.Model):
    transaction_status = [
        ("On Cart", "On Cart"),
        ("To Pay", "To Pay"),
        ("To Ship", "Cancelled"),
        ("To Receive", "To Receive"),
        ("Delivered", "Delivered"),
    ]
    buyer = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name="transactions_of_buyer",
        null=True
    ) 
    
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name="transactions_of_product",
        null=True
    ) 
    
    amount = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=transaction_status,
        default="On Cart"
    )

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        print("From models.py: ", self.product.name)
        return f"{self.product.name}"