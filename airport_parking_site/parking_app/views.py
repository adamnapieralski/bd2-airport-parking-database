from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import TicketShortForm, TicketLongForm, TicketPaymentForm, TicketExitForm, ClientForm, CarForm, ReservationForm, ReservationCarForm
from . import models
from . import ticketing
from . import report
from .reservation import check_reservation

import datetime
import math

# Create your views here.


def home(request):
    return render(request, 'parking_app/home.html')


@login_required
@user_passes_test(lambda user: not user.is_superuser)
def reservation(request):
    if request.method == "POST":
        form = ReservationCarForm(request.user, request.POST)
        if form.is_valid():


            return redirect('tickets_view_id', id=bilet.id)
    else:
        form = ReservationCarForm(request.user)

    return render(request, 'parking_app/reservation.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def reporting(request):
    table = None
    from_date = None
    to_date = None
    try:
        table = request.POST['view_table']
        from_date = request.POST['ticket_from']
        to_date = request.POST['ticket_to']
    except(KeyError):
        pass
    return render(request, 'parking_app/reporting.html', report.get_repoting_data(table, from_date, to_date))


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


def tickets(request):
    if request.method == "POST":
        form_exit = TicketExitForm(request.POST)
        if form_exit.is_valid():
            bilet = models.Bilet.objects.get(id=form_exit.cleaned_data.get('nr_biletu'))
            bilet.czas_wyjazdu = timezone.now()
            bilet.save()

            return redirect('tickets_view_id', id=bilet.id)
    else:
        form_exit = TicketExitForm()

    return render(request, 'parking_app/tickets.html', {'form_exit': form_exit})


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
                czas_wjazdu=timezone.now(),
                wykupiony_czas=0,
                nr_biletu=0,
                strefa=form.cleaned_data['strefa']
            )
            bilet.nr_biletu = bilet.id
            bilet.save()
            ticket.bilet = bilet

            rezerwacja = models.Rezerwacja.objects.filter(
                id=form.cleaned_data['rezerwacja_id']).first()
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

    datetime_payed_to = None

    if bilet is not None:
        datetime_payed_to = bilet.czas_wjazdu

        if bilet_dlugoterminowy is not None:
            datetime_payed_to = bilet_dlugoterminowy.rezerwacjaa.data_rozpoczecia

        datetime_payed_to += datetime.timedelta(seconds=bilet.wykupiony_czas*3600)

    return render(request, 'parking_app/ticket_details.html',
                  {'bilet': bilet, 'bilet_dlugoterminowy': bilet_dlugoterminowy,
                   'datetime_payed_to': datetime_payed_to})


def tickets_view_selected(request):
    ticket_id = request.POST['nrBiletu']
    return HttpResponseRedirect(reverse('tickets_view_id', args=(ticket_id,)))


def tickets_pay_id(request, id):
    bilet = models.Bilet.objects.filter(id=id).first()
    bilet_dlugoterminowy = models.BiletDlugoterminowy.objects.filter(bilet=bilet).first()
    cennik = models.Cennik.objects.filter(rodzaj_parkingu=bilet.strefa.parking.rodzaj_parkingu)

    current_time = timezone.now()
    duration = current_time - bilet.czas_wjazdu
    time_to_pay = duration.days * 24 + math.ceil(duration.seconds / 3600)

    if bilet_dlugoterminowy is not None:
        rez = models.Rezerwacja.objects.filter(id=bilet_dlugoterminowy.rezerwacjaa.id).first()
        duration = rez.data_zakonczenia - rez.data_rozpoczecia
        time_to_pay = duration.days * 24 + duration.seconds // 3600

    time_to_pay = max(0, time_to_pay - bilet.wykupiony_czas)

    if request.method == "POST":
        form = TicketPaymentForm(request.POST)
        if form.is_valid():
            oplata = form.save(commit=False)
            if bilet_dlugoterminowy is not None and time_to_pay < ticketing.calculate_paid_time(cennik, oplata.kwota_podstawowa):
                bilet.wykupiony_czas += time_to_pay
            else:
                bilet.wykupiony_czas += ticketing.calculate_paid_time(
                    cennik, oplata.kwota_podstawowa)
            bilet.save()
            oplata.bilet = bilet
            oplata.czas = timezone.now()
            oplata.kwota_ostateczna = oplata.kwota_podstawowa
            oplata.status = '1'
            oplata.save()
            return redirect('tickets_view_id', id=bilet.id)

    else:
        form = TicketPaymentForm(
            initial={'kwota_podstawowa': ticketing.calculate_min_pay_price(cennik, time_to_pay)})

    return render(request, 'parking_app/ticket_payment.html',
                  {'form': form, 'bilet': bilet, 'bilet_dlugoterminowy': bilet_dlugoterminowy, 'cennik': cennik,
                   'time_to_pay': time_to_pay, 'current_time': current_time})


def tickets_pay_selected(request):
    ticket_id = request.POST['nrBiletu']
    return HttpResponseRedirect(reverse('tickets_pay_id', args=(ticket_id,)))

def post_new(request):
    form = ClientForm()
    return render(request, 'parking_app/reservation.html', {'form': form}) 

def client_data(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client=form.save()
            return redirect('car_data', id=client.id)
    else:
        form = ClientForm()
    return render(request, 'parking_app/client_panel.html', {'form': form})  


#user,klient,id

def car_data(request,id):
    klient = models.Klient.objects.get(id=id) 
    form = CarForm(request.POST)
    if request.method == "POST":    
        if form.is_valid():
            car=form.save(commit=False)
            car.klient=klient
            car=form.save()
            request.session['numer_rejestracyjny'] = car.nr_rejestracyjny
            return redirect('make_reservation')
    else:
        form = CarForm()
    return render(request, 'parking_app/car_data.html', {'form': form}) 

def make_reservation(request):
    pojazd = models.Pojazd.objects.get(nr_rejestracyjny=request.session.get('numer_rejestracyjny'))
    typ_pojazdu=pojazd.typ_pojazdu
    klient =pojazd.klient      
    if request.method == "POST":
        form=ReservationForm(request.POST)
        if form.is_valid():
            rezerwacja=form.save(commit=False)
            #wolne_miejsce= check_reservation(rezerwacja.data_rozpoczecia,rezerwacja.data_zakonczenia,typ_pojazdu)
            if True: #wolne_miejsce!=None:
                
                rezerwacja.klient=klient  
                rezerwacja.miejsce_parkingowe=models.MiejsceParkingowe.objects.all().first()
                rezerwacja.nr_rezerwacji=0
                rezerwacja.save()
                rezerwacja.nr_rezerwacji=rezerwacja.id
                rezerwacja.save()
                return render(request,'parking_app/response_reserved.html', {'rezerwacja': rezerwacja, 'pojazd': pojazd,'miejsce':models.MiejsceParkingowe.objects.all().first()})
            #'miejsce': wolne_miejsce
                #return HttpResponseRedirect('parking_app/response_reserved')
            else:    
                #return HttpResponseRedirect('parking_app/response_no_free_places') 
                raise form.ValidationError("Nie ma wolnych miejsc w tym terminie")
        else:
            raise form.ValidationError("Błędne daty")
    else:
        form=ReservationForm()

    print(form)
    return render(request, 'parking_app/reservation.html', {'form': form})

#reservation
def see_reservations(request,id):
    aktualny_klient=models.Klient.objects.filter(id=id)
    rezerwacje=models.Rezerwacja.objects.filter(klient=aktualny_klient)
    return render(request, 'parking_app/my_reservations.html', {'rezerwacje': rezerwacje})
    
def test_myreservations(request):
    k_id=135
    return redirect('see_reservations', id= k_id)
