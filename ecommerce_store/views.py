from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # return HttpResponse("Hello, you're in Home page")
    return render(request, 'base.html')

def about(request):
    return HttpResponse("Hello, you're in about page")

def contact(request):
    return HttpResponse("Hello, you're in contact page")