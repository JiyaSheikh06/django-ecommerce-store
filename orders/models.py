import uuid
from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('confirmed',  'Confirmed'),
        ('processing', 'Processing'),
        ('shipped',    'Shipped'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]

    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_id         = models.CharField(max_length=20, unique=True, editable=False)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total            = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Shipping info
    first_name       = models.CharField(max_length=100, blank=True)
    last_name        = models.CharField(max_length=100, blank=True)
    email            = models.EmailField(blank=True)
    phone            = models.CharField(max_length=20, blank=True)
    address          = models.CharField(max_length=255, blank=True)
    city             = models.CharField(max_length=100, blank=True)
    state            = models.CharField(max_length=100, blank=True)
    zip_code         = models.CharField(max_length=20, blank=True)
    country          = models.CharField(max_length=100, blank=True)
    payment_method   = models.CharField(max_length=50, default='card')
    notes            = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = 'ORD-' + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price    = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of order

    def __str__(self):
        return f"{self.quantity} × {self.product.name if self.product else 'Deleted product'}"

    @property
    def subtotal(self):
        return self.price * self.quantity
