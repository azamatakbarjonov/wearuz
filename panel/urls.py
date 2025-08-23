from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.shop, name='shop'),
    path('create_order/', views.create_order, name='create_order'),
    path('panel/', views.panel, name='panel'),
]
