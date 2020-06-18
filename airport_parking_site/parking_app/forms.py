from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator

from . import models

import datetime

class TicketShortForm(forms.ModelForm):
    class Meta:
        model = models.Bilet
        fields = ['strefa']
    
    def __init__(self, *args, **kwargs):
        super(TicketShortForm, self).__init__(*args, **kwargs)
        self.fields['strefa'].queryset = models.Strefa.objects.filter(parking__rodzaj_parkingu="krotkoterminowy")


class TicketLongForm(forms.ModelForm):
    rezerwacja_id = forms.IntegerField(validators=[MinValueValidator(1)])
    class Meta:
        model = models.BiletDlugoterminowy
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

class TicketExitForm(forms.Form):
    nr_biletu = forms.IntegerField(label='', 
                                    widget=forms.TextInput(attrs={'placeholder': 'Podaj numer biletu...'}),
                                    validators=[MinValueValidator(1)])
    
    def clean_nr_biletu(self):
        nr_biletu = self.cleaned_data.get('nr_biletu')

        bilet = models.Bilet.objects.filter(id=nr_biletu).first()

        if bilet is None:
            raise forms.ValidationError("Podany bilet nie istnieje.")

        bilet_dlugoterminowy = models.BiletDlugoterminowy.objects.filter(bilet=bilet).first()

        curr_time = timezone.now()

        wykupiony_czas_d = datetime.timedelta(seconds=bilet.wykupiony_czas*3600)

        if bilet.czas_wjazdu > curr_time:
            raise forms.ValidationError("Niepoprawny bilet.")

        if bilet_dlugoterminowy is not None:
            if curr_time > bilet_dlugoterminowy.rezerwacjaa.data_zakonczenia:
                raise forms.ValidationError("Minął termin rezerwacji.")
            if curr_time > bilet_dlugoterminowy.rezerwacjaa.data_rozpoczecia + wykupiony_czas_d:
                raise forms.ValidationError("Bilet nieopłacony.")
        
        if curr_time > bilet.czas_wjazdu + wykupiony_czas_d:
            raise forms.ValidationError("Bilet nieopłacony.")

        return nr_biletu


class TicketPaymentForm(forms.ModelForm):
    class Meta:
        model = models.Oplata
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
