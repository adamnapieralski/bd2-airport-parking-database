from django.shortcuts import render
from django.http import HttpResponse
from . import ticketing

# Create your views here.

def index(request):
    return HttpResponse("Index")

def tickets(request):
    table = None
    try:
        table = request.POST['view_table']
    except(KeyError):
        pass
    return render(request, 'parking_app/tickets.html', ticketing.get_data(table)) 
    # return render(request, 'parking_app/tickets.html')