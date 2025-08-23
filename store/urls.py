# store/urls.py

from django.urls import path
from .views import ProductListView, OrderCreateAPIView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('order/', OrderCreateAPIView.as_view(), name='order-create'),
]
