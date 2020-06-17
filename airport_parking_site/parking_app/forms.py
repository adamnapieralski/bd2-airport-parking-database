from django import forms
from .models import Bilet, BiletDlugoterminowy, Oplata
from . import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

import datetime

class TicketShortForm(forms.ModelForm):
    class Meta:
        model = Bilet
        fields = ['strefa']
    
    def __init__(self, *args, **kwargs):
        super(TicketShortForm, self).__init__(*args, **kwargs)
        self.fields['strefa'].queryset = models.Strefa.objects.filter(parking__rodzaj_parkingu="krotkoterminowy")


class TicketLongForm(forms.ModelForm):
    rezerwacja_id = forms.IntegerField()
    class Meta:
        model = BiletDlugoterminowy
        fields = []
    
    def __init__(self, *args, **kwargs):
        super(TicketLongForm, self).__init__(*args, **kwargs)
        self.fields['strefa']=forms.ModelChoiceField(queryset=models.Strefa.objects.filter(parking__rodzaj_parkingu="dlugoterminowy"))

    def clean_rezerwacja_id(self):
        rezerwacja_id = self.cleaned_data.get('rezerwacja_id')
        
        if not models.Rezerwacja.objects.filter(id=rezerwacja_id).exists():
            raise forms.ValidationError("Rezerwacja o podanym ID nie istnieje.")

        current_time = timezone.now()
        rezerwacja = models.Rezerwacja.objects.get(id=rezerwacja_id)

        if rezerwacja.data_rozpoczecia > current_time or rezerwacja.data_zakonczenia < current_time:
            raise forms.ValidationError("Podana rezerwacja w tym momencie nie obowiązuje.")

        if rezerwacja.bilet_dlugoterminowy is not None:
            raise forms.ValidationError("Bilet dla tej rezerwacji został już pobrany.")

        return rezerwacja_id

    def clean_strefa(self):
        rezerwacja_id = self.cleaned_data.get('rezerwacja_id')
        strefa = self.cleaned_data.get('strefa')

        if not models.Rezerwacja.objects.filter(id=rezerwacja_id, miejsce_parkingowe__strefa=strefa).exists():
            raise forms.ValidationError("Ta rezerwacja obowiązuje na innej strefie.")

        return strefa

class TicketPaymentForm(forms.ModelForm):
    class Meta:
        model = Oplata
        fields = ['metoda_platnosci', 'kwota_podstawowa']
        labels = {
            'metoda_platnosci': _('Metoda płatności'),
            'kwota_podstawowa': _('Kwota'),
        }

    def clean_kwota_podstawowa(self):
        kwota = self.cleaned_data.get('kwota_podstawowa')
        if kwota < 0 or not (100*kwota).is_integer():
            print(kwota)
            raise forms.ValidationError("Niepoprawna kwota.")
        return kwota
