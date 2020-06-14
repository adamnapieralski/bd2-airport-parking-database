from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import ticketing
from .forms import TicketShortForm, TicketLongForm
from django.utils import timezone
from . import models

# Create your views here.

def index(request):
    return HttpResponse("Index")

def tickets(request):
    return render(request, 'parking_app/tickets.html', ticketing.get_data()) 
    # return render(request, 'parking_app/tickets.html')

def ticket_new_short(request):
    if request.method == "POST":
        form = TicketShortForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.czas_wjazdu = timezone.now()
            ticket.wykupiony_czas = 15
            ticket.nr_biletu = 0
            ticket.czas_wyjazdu = timezone.now()
            ticket.save()
            ticket.nr_biletu = ticket.id
            ticket.save()
            return redirect('ticket_detail', id=ticket.id)
    else:
        form = TicketShortForm()

    # form = TicketShortForm()
    return render(request, 'parking_app/ticket_new_short.html', {'form': form})

def ticket_new_long(request):
    form = TicketLongForm()
    return render(request, 'parking_app/ticket_new_long.html', {'form': form})

def ticket_detail(request, id):
    bilet = models.Bilet.objects.get(id=id)
    
    return render(request, 'parking_app/ticket_details.html', {'bilet': bilet})
    # return HttpResponse("Details")


# def tickets_add_ticket(request):
#     try:
#         strefa = request.POST['strefa']
#         return ticketing.add_ticket(strefa)
#     except(KeyError):
#         return tickets(request)