from django.shortcuts import render
from django.http import HttpResponse

from . import report

# Create your views here.

def index(request):
    return HttpResponse("Index")

def tickets(request):
    return HttpResponse("Tickets")

def reporting(request):    
    return render(request, 'parking_app/reporting.html', report.get_db_stats()) 

def reporting_download_stats(request):
    try:
        type = request.POST['stats_download']
        return report.export_stats_to_csv(type)
    except(KeyError):
        return reporting(request)
