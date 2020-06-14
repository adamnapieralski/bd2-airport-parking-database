from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.


def home(request):
    return render(request, 'parking_app/home.html')


@login_required
@user_passes_test(lambda u: not u.is_superuser)
def home_client(request):
    return render(request, 'parking_app/home_cl.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def home_admin(request):
    return render(request, 'parking_app/home_ad.html')


def ticket(request):
    return render(request, 'parking_app/ticket.html')


@login_required
@user_passes_test(lambda u: not u.is_superuser)
def reservation(request):
    return render(request, 'parking_app/reservation.html')


@login_required
@user_passes_test(lambda user: user.is_superuser)
def report(request):
    return render(request, 'parking_app/report.html')
