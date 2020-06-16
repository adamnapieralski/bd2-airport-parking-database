from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import ticketing
from .forms import TicketShortForm, TicketLongForm, TicketPaymentForm
from django.utils import timezone
from . import models
from django.urls import reverse

from datetime import datetime
import math


# Create your views here.

def index(request):
    return HttpResponse("Index")

def tickets(request):
    return render(request, 'parking_app/tickets.html', ticketing.get_data()) 

def tickets_new_shortterm(request):
    if request.method == "POST":
        form = TicketShortForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.czas_wjazdu = timezone.now()
            ticket.wykupiony_czas = 0
            ticket.nr_biletu = 0
            ticket.save()
            ticket.nr_biletu = ticket.id
            ticket.save()
            return redirect('tickets_view_id', id=ticket.id)
    else:
        form = TicketShortForm()

    return render(request, 'parking_app/ticket_new_short.html', {'form': form})

def tickets_new_longterm(request):
    if request.method == "POST":
        form = TicketLongForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            bilet = models.Bilet.objects.create(
                czas_wjazdu = timezone.now(),
                wykupiony_czas = 0,
                nr_biletu = 0,
                strefa = form.cleaned_data['strefa']
            )
            bilet.nr_biletu = bilet.id
            bilet.save()
            ticket.bilet = bilet

            rezerwacja = models.Rezerwacja.objects.filter(id=form.cleaned_data['rezerwacja_id']).first()
            ticket.rezerwacjaa = rezerwacja
            ticket.save()
            rezerwacja.bilet_dlugoterminowy = ticket
            rezerwacja.save()

            return redirect('tickets_view_id', id=ticket.bilet.id)
    else:
        form = TicketLongForm()

    return render(request, 'parking_app/ticket_new_long.html', {'form': form})

def tickets_view_id(request, id):
    bilet = models.Bilet.objects.filter(id=id).first()

    bilet_dlugoterminowy = models.BiletDlugoterminowy.objects.filter(bilet=bilet).first()
    
    return render(request, 'parking_app/ticket_details.html',
                {'bilet': bilet, 'bilet_dlugoterminowy': bilet_dlugoterminowy})

def tickets_view_selected(request):
    ticket_id = request.POST['nrBiletu']
    return HttpResponseRedirect(reverse('tickets_view_id', args=(ticket_id,)))

def tickets_pay_id(request, id):
    bilet = models.Bilet.objects.filter(id=id).first()
    bilet_dlugoterminowy = models.BiletDlugoterminowy.objects.filter(bilet=bilet).first()
    cennik = models.Cennik.objects.filter(rodzaj_parkingu=bilet.strefa.parking.rodzaj_parkingu)

    duration = timezone.now() - bilet.czas_wjazdu
    czas_do_oplaty = math.ceil(duration.days * 24 + duration.seconds // 3600)

    if bilet_dlugoterminowy is not None:
        rez = models.Rezerwacja.objects.filter(id=bilet_dlugoterminowy.rezerwacjaa.id).first()
        duration = rez.data_zakonczenia - rez.data_rozpoczecia
        czas_do_oplaty = duration.days * 24 + duration.seconds // 3600

    czas_do_oplaty = max(0, czas_do_oplaty - bilet.wykupiony_czas)

    if request.method == "POST":
        form = TicketPaymentForm(request.POST)
        if form.is_valid():
            oplata = form.save(commit=False)
            bilet.wykupiony_czas += ticketing.calculate_paid_time(cennik, oplata.kwota_podstawowa)
            bilet.save()
            oplata.bilet = bilet
            oplata.czas = timezone.now()
            oplata.kwota_ostateczna = oplata.kwota_podstawowa
            oplata.status = '1'
            oplata.save()
            return redirect('tickets_view_id', id=bilet.id)

    else:
        form = TicketPaymentForm(initial={'kwota_podstawowa': ticketing.calculate_min_pay_price(cennik, czas_do_oplaty)})

    return render(request, 'parking_app/ticket_payment.html',
    {'form': form, 'bilet': bilet, 'bilet_dlugoterminowy': bilet_dlugoterminowy, 'cennik': cennik,
    'czas_do_oplaty': czas_do_oplaty, })

def tickets_pay_selected(request):
    ticket_id = request.POST['nrBiletu']
    return HttpResponseRedirect(reverse('tickets_pay_id', args=(ticket_id,)))