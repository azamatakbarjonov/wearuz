from django.shortcuts import render
from .models import Trend, Box, Headnav

def home_view(request):
    sect = Trend.objects.all()
    box = Box.objects.all()
    head = Headnav.objects.first()
    context = {
        'sect':sect,
        'box':box,
        'head':head,
    }
    return render(request, 'home.html',context)
