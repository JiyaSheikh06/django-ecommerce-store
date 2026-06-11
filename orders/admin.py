from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model      = OrderItem
    extra      = 0
    fields     = ('product', 'quantity', 'price')
    readonly_fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display   = ('order_id', 'user', 'total', 'status', 'created_at')
    list_filter    = ('status',)
    search_fields  = ('order_id', 'user__username', 'email')
    list_editable  = ('status',)
    readonly_fields = ('order_id', 'created_at', 'updated_at')
    inlines        = [OrderItemInline]
    ordering       = ('-created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'subtotal')
