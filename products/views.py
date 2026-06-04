from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request, 'products/home.html')

def product_detail_view(request):
    return render(request,'products/product_detail.html')

def product_list_view(request):
    return render(request, 'products/product_list.html')