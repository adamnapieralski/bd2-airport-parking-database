from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import ClientForm
from .forms import CarForm
from .forms import ReservationForm
from . import models
from .tickets import check_reservation
from django.shortcuts import redirect


# Create your views here.

def index(request):
    return HttpResponse("Index")

def tickets(request):
    return render(request, 'parking_app/reservation.html', tickets.get_data());    
    
def post_new(request):
    form = ClientForm()
    return render(request, 'parking_app/tickets.html', {'form': form}) 

def client_data(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client=form.save()
            return redirect('car_data', id=client.id)
    else:
        form = ClientForm()
    return render(request, 'parking_app/client_panel.html', {'form': form})  


def car_data(request,id):
    klient = models.Klient.objects.get(id=id) 
    form = CarForm(request.POST)
    if request.method == "POST":    
        if form.is_valid():
            car=form.save(commit=False)
            car.foreignkeytoKlient=id
            car=form.save()
            return redirect('make_reservation', id= car.id)
    else:
        form = CarForm()
    return render(request, 'parking_app/car_data.html', {'form': form}) 



def make_reservation(request, id):
    pojazd = models.Pojazd.objects.get(id=id)
    typ_pojazdu=pojazd.typ_pojazdu
    klient =pojazd.Klient      
    form=ReservationForm(request.POST)
    #ReservationInlineFormSet = inlineformset_factory(klient, models.Rezerwacja,fk_name=id, fields=('data_rozpoczecia','data_zakonczenia'))
    if request.method == "POST":
        #formset = ReservationInlineFormSet(request.POST, request.FILES, instance=klient)
        if form.is_valid():
            wolne_miejsce= check_reservation(form.data_rozpoczecia,form.data_zakonczenia,typ_pojazdu)
            if wolne_miejsce!=None:
                rezerwacja=form.save(commit=False)
                rezerwacja.foreignkeytoKlient=klient.id  
                rezerwacja.nr_rezerwacji=0
                rezerwacja.save()
                rezerwacja.nr_rezerwacji=rezerwacja.id
                rezerwacja.save()
                return redirect( 'parking_app/response_reserved.html', {'rezerwacja': rezerwacja, 'pojazd': pojazd,
                'miejsce': wolne_miejsce})
                #return HttpResponseRedirect('parking_app/response_reserved')
            else:    
                return HttpResponseRedirect('parking_app/response_no_free_places') 
    else:
        form=ReservationForm(request.POST)
        #forms = ReservationInlineFormSet(instance=klient)
    return render(request, 'parking_app/tickets.html', {'form': form})


def see_reservations(request,id):
    aktualny_klient=models.Klient.objects.filter(id=id)
    rezerwacje=models.Rezerwacja.objects.filter(klient=aktualny_klient)
    return redirect( 'parking_app/my_reservations.html', {'rezerwacje': rezerwacje})
    
def test_myreservations(request):
    k_id=135
    return redirect('see_reservations', id= k_id)
    

# class DeleteView(SuccessMessageMixin, DeleteView):
# model = OrderSparePart
# success_url = '/'
# success_message = "deleted..."

# def delete(self, request, *args, **kwargs):
#     self.object = self.get_object()
#     name = self.object.name
#     request.session['name'] = name  # name will be change according to your need
#     message = request.session['name'] + ' deleted successfully'
#     messages.success(self.request, message)
#     return super(DeleteView, self).delete(request, *args, **kwargs
    
    
    


#Łukasza
#def reporting(request):    
#   return render(request, 'parking_app/reporting.html', report.get_db_stats()) 

#def reporting_download_stats(request):
#   return report.export_stats_to_csv()
