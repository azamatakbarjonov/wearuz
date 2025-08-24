from rest_framework import serializers
from .models import Product, ProductStock, Order


class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = ["size", "quantity"]


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'price', 'category', 'stocks']

    def get_image(self, obj):
        try:
            if obj.image and hasattr(obj.image, "cdn_url"):
                return obj.image.cdn_url  # ✅ to‘g‘ri
        except Exception:
            return None
        return None






class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'customer_name',
            'customer_phone',
            'customer_address',
            'data',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        basket = validated_data.pop("data", {})  # JSON ichidagi savat

        # Buyurtma yaratamiz
        order = Order.objects.create(**validated_data)

        # Har bir mahsulotni stokdan kamaytiramiz
        for key, item in basket.items():
            pid = item["id"]
            size = item["size"]
            qty = int(item["qty"])

            try:
                stock = ProductStock.objects.get(product_id=pid, size=size)
            except ProductStock.DoesNotExist:
                raise serializers.ValidationError(
                    f"Stok topilmadi (ID: {pid}, Size: {size})"
                )

            if stock.quantity < qty:
                raise serializers.ValidationError(
                    f"{stock.product.name} ({size}) uchun yetarli emas! "
                    f"Bor: {stock.quantity} ta"
                )

            stock.quantity -= qty
            stock.save()

        return order

# from rest_framework import serializers
# from .models import Product, ProductStock, Order

# class ProductStockSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductStock
#         fields = ['size', 'quantity']

# class ProductSerializer(serializers.ModelSerializer):
#     stocks = ProductStockSerializer(many=True, read_only=True)
#     image = serializers.ImageField(use_url=True)

#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'image', 'price', 'category', 'stocks']

# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ['id', 'customer_name', 'customer_phone', 'customer_address', 'data', 'created_at']
#         read_only_fields = ['id', 'created_at']

#     def create(self, validated_data):
#         basket = validated_data.get("data", [])

#         order = Order.objects.create(**validated_data)

#         # Stoklarni kamaytirish
#         for item in basket:
#             pid = item['id']
#             size = item['size']
#             qty = int(item['qty'])

#             try:
#                 stock = ProductStock.objects.get(product_id=pid, size=size)
#             except ProductStock.DoesNotExist:
#                 raise serializers.ValidationError(f"Stok topilmadi (ID: {pid}, Size: {size})")

#             if stock.quantity < qty:
#                 raise serializers.ValidationError(
#                     f"{stock.product.name} ({size}) uchun yetarli emas! Bor: {stock.quantity} ta"
#                 )

#             stock.quantity -= qty
#             stock.save()

#         return order
