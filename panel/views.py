from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from store.models import Order, Product, ProductStock
import json

# Shop sahifasi
def shop(request):
    products = Product.objects.prefetch_related('stocks').all()
    return render(request, 'shop.html', {'products': products})

# Buyurtma yaratish (AJAX orqali)
@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('customer_name')
            phone = data.get('customer_phone')
            address = data.get('customer_address')
            cart = data.get('data', {})

            if not (name and phone and address and cart):
                return JsonResponse({'status':'error', 'message':'Ma\'lumot yetarli emas yoki savatcha bo\'sh'})

            # Order yaratish
            order = Order.objects.create(
                customer_name=name,
                customer_phone=phone,
                customer_address=address,
                data=cart
            )

            # Stokni kamaytirish
            for key, item in cart.items():
                pid = item['id']
                size = item['size']
                qty = int(item['qty'])
                stock = ProductStock.objects.get(product_id=pid, size=size)
                stock.quantity -= qty
                stock.save()

            return JsonResponse({'status':'success', 'message':'Buyurtma qabul qilindi!', 'order_id': order.id})
        except Exception as e:
            print("Order xatosi:", e)
            return JsonResponse({'status':'error', 'message': str(e)})

    return JsonResponse({'status':'error', 'message':'POST method kerak'})

# Kasser paneli
def panel(request):
    orders = Order.objects.order_by('-created_at')
    return render(request, 'panel.html', {'orders': orders})
