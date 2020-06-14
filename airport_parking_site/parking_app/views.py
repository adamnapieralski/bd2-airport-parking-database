from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from .forms import PostForm
from . import models
from .tickets import check_reservation
from django.shortcuts import redirect


# Create your views here.

def index(request):
    return HttpResponse("Index")

def tickets(request):
    return render(request, 'parking_app/reservation.html', tickets.get_data());    
    
def post_new(request):
    form = PostForm()
    return render(request, 'parking_app/tickets.html', {'form': form}) 

def client_data(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('make_reservation', pk=form.pk)
    else:
        form = PostForm()
    return render(request, 'parking_app/client_panel.html', {'form': form})    



def make_reservation(request, klient_id):
    klient = models.Klient.objects.get(pk=klient_id)
    ReservationInlineFormSet = inlineformset_factory(klient, models.Rezerwacja, fields=('data_rozpoczecia','data_zakonczenia'))
    if request.method == "POST":
        formset = ReservationInlineFormSet(request.POST, request.FILES, instance=klient)
        if formset.is_valid():
            if check_reservation():
                formset.save()
                # Do something. Should generally end with a redirect. For example:
                return HttpResponseRedirect('parking_app/response_reserved')
            else:    
                return HttpResponseRedirect('parking_app/response_no_free_places') 
    else:
        formset = ReservationInlineFormSet(instance=klient)
    return render(request, 'parking_app/tickets2', {'formset': formset})


def post_results(request):
    return render(request, 'parking_app/reservation_results.html', tickets.check_reservation());
    


#Łukasza
#def reporting(request):    
#   return render(request, 'parking_app/reporting.html', report.get_db_stats()) 

#def reporting_download_stats(request):
#   return report.export_stats_to_csv()
