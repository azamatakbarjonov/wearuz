from django.shortcuts import render

def shop_view(request):
    context = {

    }
    return render(request, 'shop.html',context)