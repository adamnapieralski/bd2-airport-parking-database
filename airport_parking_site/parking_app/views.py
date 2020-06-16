from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from . import report

def tickets(request):
    return HttpResponse("Tickets")

def home(request):
    return render(request, 'parking_app/home.html')

def ticket(request):
    return render(request, 'parking_app/ticket.html')

@login_required
@user_passes_test(lambda u: not u.is_superuser)
def reservation(request):
    return render(request, 'parking_app/reservation.html')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def reporting(request):
    table = None
    try:
        table = request.POST['view_table']
    except(KeyError):
        pass
    return render(request, 'parking_app/reporting.html', report.get_repoting_data(table)) 

@login_required
@user_passes_test(lambda user: user.is_superuser)
def reporting_download_stats(request):
    try:
        type = request.POST['stats_download']
        return report.export_stats_to_csv(type)
    except(KeyError):
        return reporting(request)
 
@login_required
@user_passes_test(lambda user: user.is_superuser)
def reporting_download_data(request):
    try:
        table = request.POST['tables']
        return report.download_table(table)
    except(KeyError):
        return reporting(request)
