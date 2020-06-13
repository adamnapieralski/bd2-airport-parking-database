from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, 'parking_app/home.html')


def home_client(request):
    return render(request, 'parking_app/home_cl.html')


def home_admin(request):
    return render(request, 'parking_app/home_ad.html')
