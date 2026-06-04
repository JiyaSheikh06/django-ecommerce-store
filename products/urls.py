from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('product_detail/', views.product_detail_view, name='product_detail'),
    path('product_list/', views.product_list_view, name='product_list'),
]