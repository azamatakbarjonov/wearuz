from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction
from .models import Product, ProductStock, Order
from .serializers import ProductSerializer, OrderSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        basket = request.data.get("data")
        name = request.data.get("customer_name")
        phone = request.data.get("customer_phone")
        address = request.data.get("customer_address")

        if not (basket and name and phone and address):
            return Response(
                {"error": "❌ Ma'lumot yetarli emas yoki savatcha bo'sh"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                product_ids = [item["id"] for item in basket.values()]
                products = Product.objects.filter(id__in=product_ids)
                products_dict = {p.id: p for p in products}

                cart_with_names = {}
                for key, item in basket.items():
                    pid = item["id"]
                    size = item["size"]
                    requested_qty = int(item["qty"])
                    
                    # 🔒 stokni lock bilan olib kelamiz
                    stock = ProductStock.objects.select_for_update().filter(
                        product_id=pid, size=size
                    ).first()

                    if not stock:
                        return Response(
                            {"error": f"❌ Stok topilmadi (id={pid}, size={size})"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    # 🔑 Agar so‘ralgan qty > stok bo‘lsa, avtomatik kamaytiramiz
                    final_qty = requested_qty
                    if stock.quantity < requested_qty:
                        final_qty = stock.quantity  # faqat mavjudini oladi

                    if final_qty <= 0:
                        return Response(
                            {"error": f"❌ {stock.product.name} ({size}) qolmagan"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    product = products_dict.get(pid)
                    if not product:
                        return Response(
                            {"error": f"❌ Mahsulot topilmadi (id={pid})"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    cart_with_names[key] = {
                        "id": pid,
                        "name": product.name,
                        "price": float(product.price),
                        "size": size,
                        "qty": final_qty,  # ✅ avtomatik kamaytirilgan qiymat
                    }

                if not cart_with_names:
                    return Response(
                        {"error": "❌ Savatcha bo'sh"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # ✅ Buyurtma yaratish
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    customer_name=name,
                    customer_phone=phone,
                    customer_address=address,
                    data=cart_with_names,
                )

                # ✅ Stokni kamaytirish
                for item in cart_with_names.values():
                    stock = ProductStock.objects.get(
                        product_id=item["id"], size=item["size"]
                    )
                    stock.quantity -= item["qty"]
                    stock.save()

        except Exception as e:
            return Response(
                {"error": f"❌ Xatolik yuz berdi: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "✅ Buyurtma qabul qilindi! Agar ba'zi mahsulotlar yetarli bo‘lmasa, avtomatik kamaytirildi.",
                "order_id": order.id,
                "cart": cart_with_names,  # user ko‘rishi uchun qaytaramiz
            },
            status=status.HTTP_201_CREATED,
        )
