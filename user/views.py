import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from panel.models import Order

from .forms import CustomLoginForm, RegisterForm,  EditProfileForm
from store.models import Order, Product

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("user:profile")
    else:
        form = RegisterForm()
    return render(request, "user/register.html", {"form": form})

def login_view(request):
    
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)  # shu yerda ham CustomLoginForm
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("user:profile")  # login bo‘lgandan keyin profile sahifasiga o‘tadi
    else:
        form = CustomLoginForm()  # GET bo‘lsa oddiy bo‘sh formani chiqaradi
    return render(request, "user/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("user:login")


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    for order in orders:
        total_price = 0
        # order.data string bo‘lsa json.loads qilamiz
        data = order.data if isinstance(order.data, dict) else json.loads(order.data)

        # mahsulotlarni boyitib chiqamiz
        for key, item in data.items():
            product = Product.objects.get(id=item['id'])
            item['name'] = product.name
            item['image'] = product.image.url
            item['price'] = float(product.price)
            item['total'] = item['price'] * int(item['qty'])
            total_price += item['total']

        # order ga qayta saqlab qo‘yish
        order.data_items = data.values()  # 👈 template’da ishlatamiz
        order.total_price = total_price

    return render(request, 'user/profile.html', {'orders': orders})


@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user:profile")
    else:
        form = EditProfileForm(instance=user)
    return render(request, "user/edit_profile.html", {"form": form})



from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def all_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, "user/alluser.html", {"users": users})