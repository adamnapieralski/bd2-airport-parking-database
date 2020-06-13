from django.shortcuts import render
from django.http import HttpResponse

from . import report

# Create your views here.

def index(request):
    return HttpResponse("Index")

def tickets(request):
    return HttpResponse("Tickets")

def reporting(request):    
    table = None
    try:
        table = request.POST['view_table']
    except(KeyError):
        pass
    return render(request, 'parking_app/reporting.html', report.get_repoting_data(table)) 

def reporting_download_stats(request):
    try:
        type = request.POST['stats_download']
        return report.export_stats_to_csv(type)
    except(KeyError):
        return reporting(request)

def reporting_download_data(request):
    try:
        table = request.POST['tables']
        return report.download_table(table)
    except(KeyError):
        return reporting(request)
