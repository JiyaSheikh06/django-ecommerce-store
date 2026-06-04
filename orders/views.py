from django.shortcuts import render

# Create your views here.
def checkout_view(request):
    return render(request, 'orders/checkout.html')

def order_history_view(request):
    return render(request,'orders/order_history.html')

def order_success_view(request):
    return render(request, 'orders/order_success.html')