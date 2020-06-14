from django.shortcuts import render
from django.http import HttpResponse
from . import ticketing
from .forms import TicketShortForm, TicketLongForm

# Create your views here.

def index(request):
    return HttpResponse("Index")

def tickets(request):
    return render(request, 'parking_app/tickets.html', ticketing.get_data()) 
    # return render(request, 'parking_app/tickets.html')

def ticket_new_short(request):
    form = TicketShortForm()
    return render(request, 'parking_app/ticket_new_short.html', {'form': form})

def ticket_new_long(request):
    form = TicketLongForm()
    return render(request, 'parking_app/ticket_new_long.html', {'form': form})


# def tickets_add_ticket(request):
#     try:
#         strefa = request.POST['strefa']
#         return ticketing.add_ticket(strefa)
#     except(KeyError):
#         return tickets(request)