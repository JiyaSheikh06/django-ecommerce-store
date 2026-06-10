from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    featured = Product.objects.filter(stock__gt=0)[:4]
    return render(request, 'products/home.html', {
        'featured_products': featured,
    })


def product_list_view(request):
    products = Product.objects.all()

    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(name__icontains=q)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')

    return render(request, 'products/product_list.html', {
        'products': products,
    })


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related = Product.objects.filter(stock__gt=0).exclude(pk=pk)[:4]
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related,
    })
