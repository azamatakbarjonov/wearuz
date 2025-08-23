from django.db import models
from django.conf import settings


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('krasovka', 'Krasovka'),
        ('shim', 'Shim'),
        ('kiyim', 'Kiyim'),
        ('kurtka', 'Kurtka'),
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class ProductStock(models.Model):
    SIZE_CHOICES = [
        ('XL', 'XL'),
        ('L', 'L'),
        ('M', 'M'),
        ('3XL', '3XL'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stocks")
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.size}"





class Order(models.Model):

    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    customer_address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict)


    def __str__(self):
        return f"{self.customer_name} — {self.created_at.strftime('%Y-%m-%d')}"



from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('krasovka', 'Krasovka'),
        ('shim', 'Shim'),
        ('kiyim', 'Kiyim'),
        ('kurtka', 'Kurtka'),
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class ProductStock(models.Model):
    SIZE_CHOICES = [
        ('XL', 'XL'),
        ('L', 'L'),
        ('M', 'M'),
        ('3XL', '3XL'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stocks")
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.size}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    customer_address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict)


    def __str__(self):
        return f"{self.customer_name} — {self.created_at.strftime('%Y-%m-%d')}"
