from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('order_detail/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('order_history/', views.order_history_view, name='order_history'),
    path('order_success/', views.order_success_view, name='order_success'),
]