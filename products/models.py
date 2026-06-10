from django.db import models


class Product(models.Model):
    name        = models.CharField(max_length=255)
    price       = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    image       = models.ImageField(upload_to='products/', blank=True, null=True)
    stock       = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        return self.stock > 0
