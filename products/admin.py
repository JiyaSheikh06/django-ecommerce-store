from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('name', 'price', 'stock', 'created_at')
    list_filter   = ('stock',)
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock')
    ordering      = ('-created_at',)
