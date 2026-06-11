# from django.shortcuts import render

# # Create your views here.
# def checkout_view(request):
#     return render(request, 'orders/checkout.html')

# def order_detail_view(request):
#     return render(request,'orders/order_detail.html')

# def order_history_view(request):
#     return render(request,'orders/order_history.html')

# def order_success_view(request):
#     return render(request, 'orders/order_success.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from cart.models import Cart, CartItem
from .models import Order, OrderItem


@login_required
def checkout_view(request):
    try:
        cart = Cart.objects.prefetch_related('items__product').get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    items = cart.items.all()
    if not items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    subtotal = cart.total
    tax = round(subtotal * 10 / 100, 2)
    shipping = 0 if subtotal >= 50 else 5
    order_total = round(subtotal + tax + shipping, 2)

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'cart_items': items,
        'cart_total': subtotal,
        'tax': tax,
        'shipping': shipping,
        'order_total': order_total,
    })


@login_required
def place_order(request):
    if request.method != 'POST':
        return redirect('checkout')

    try:
        cart = Cart.objects.prefetch_related('items__product').get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    items = cart.items.all()
    if not items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    # Validate stock before placing order
    for item in items:
        if item.product.stock < item.quantity:
            messages.error(
                request,
                f'Sorry, only {item.product.stock} unit(s) of "{item.product.name}" available.'
            )
            return redirect('cart')

    subtotal = cart.total
    tax = round(subtotal * 10 / 100, 2)
    shipping = 0 if subtotal >= 50 else 5
    order_total = round(subtotal + tax + shipping, 2)

    with transaction.atomic():
        order = Order.objects.create(
            user           = request.user,
            total          = order_total,
            first_name     = request.POST.get('first_name', ''),
            last_name      = request.POST.get('last_name', ''),
            email          = request.POST.get('email', ''),
            phone          = request.POST.get('phone', ''),
            address        = request.POST.get('address', ''),
            city           = request.POST.get('city', ''),
            state          = request.POST.get('state', ''),
            zip_code       = request.POST.get('zip_code', ''),
            country        = request.POST.get('country', ''),
            payment_method = request.POST.get('payment_method', 'card'),
            notes          = request.POST.get('notes', ''),
        )

        for item in items:
            OrderItem.objects.create(
                order    = order,
                product  = item.product,
                quantity = item.quantity,
                price    = item.product.price,
            )
            # Decrease stock
            item.product.stock -= item.quantity
            item.product.save()

        # Clear the cart
        cart.items.all().delete()

    messages.success(request, f'Order {order.order_id} placed successfully!')
    return redirect('order_success', pk=order.pk)


@login_required
def order_success_view(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_history_view(request):
    orders = request.user.orders.prefetch_related('items__product').all()
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
