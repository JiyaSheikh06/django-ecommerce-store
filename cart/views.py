from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from products.models import Product
from .models import Cart, CartItem


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_view(request):
    cart = get_or_create_cart(request.user)
    items = cart.items.select_related('product').all()

    subtotal = cart.total
    tax = round(subtotal * 10 / 100, 2)
    order_total = round(subtotal + tax, 2)

    # Free shipping over Rs. 15000
    shipping = 0 if subtotal >= 15000 else 500
    order_total = round(subtotal + tax + shipping, 2)

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'cart_items': items,
        'cart_total': subtotal,
        'tax': tax,
        'shipping': shipping,
        'order_total': order_total,
    })


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if not product.in_stock:
        messages.error(request, f'"{product.name}" is out of stock.')
        return redirect('product_detail', pk=pk)

    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    cart = get_or_create_cart(request.user)

    with transaction.atomic():
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            new_qty = item.quantity + quantity
            if new_qty > product.stock:
                messages.warning(request, f'Only {product.stock} units available.')
                item.quantity = product.stock
            else:
                item.quantity = new_qty
        else:
            if quantity > product.stock:
                item.quantity = product.stock
                messages.warning(request, f'Only {product.stock} units available.')
            else:
                item.quantity = quantity
        item.save()

    messages.success(request, f'"{product.name}" added to cart.')
    return redirect('cart')


@login_required
def update_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        if item.quantity < item.product.stock:
            item.quantity += 1
            item.save()
        else:
            messages.warning(request, 'Maximum available stock reached.')
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
            messages.success(request, 'Item removed from cart.')

    return redirect('cart')


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
def clear_cart(request):
    cart = get_or_create_cart(request.user)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared.')
    return redirect('cart')
