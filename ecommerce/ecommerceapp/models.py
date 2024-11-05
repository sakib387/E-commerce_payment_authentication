from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=100)
    category=models.CharField(max_length=100,default="")
    subcategory=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=300)
    image=models.ImageField(upload_to='images/images')

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} ({self.quantity})"
    @property
    def total_price(self):
        return self.quantity * self.product.price
    
class Order(models.Model):
    ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"
