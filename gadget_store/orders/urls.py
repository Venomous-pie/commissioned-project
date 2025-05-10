# orders/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('complete/<int:order_id>/', views.order_complete, name='order_complete'),
    path('history/', views.order_history, name='order_history'),
]