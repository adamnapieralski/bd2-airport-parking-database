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

    return render(request, 'parking_app/ticket_new_short.html', {'form': form})

def ticket_new_long(request):
    if request.method == "POST":
        form = TicketLongForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket = models.Rezerwacja.objects.filter(id=form.cleaned_data['rezerwacja_id']).first().bilet_dlugoterminowy
            ticket.bilet.czas_wjazdu = timezone.now()
            ticket.bilet.czas_wyjazdu = timezone.now()
            ticket.save()
            print(ticket.bilet.czas_wjazdu)
            return redirect('ticket_detail', id=ticket.bilet.id)
    else:
        form = TicketLongForm()

    return render(request, 'parking_app/ticket_new_long.html', {'form': form})

def ticket_detail(request, id):
    bilet = models.Bilet.objects.get(id=id)

    bilet_dlugoterminowy = models.BiletDlugoterminowy.objects.filter(bilet=bilet).first()
    
    return render(request, 'parking_app/ticket_details.html',
                {'bilet': bilet, 'bilet_dlugoterminowy': bilet_dlugoterminowy})