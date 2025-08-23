from django.contrib import admin
from .models import Product, ProductStock

class ProductStockInline(admin.TabularInline):
    model = ProductStock
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    inlines = [ProductStockInline]

admin.site.register(ProductStock)
