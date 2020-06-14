from django import forms
from .models import Bilet, BiletDlugoterminowy
from . import models

class TicketShortForm(forms.ModelForm):
    class Meta:
        model = Bilet
        fields = ['strefa']
    
    def __init__(self):
        super(TicketShortForm, self).__init__()
        self.fields['strefa'].queryset = models.Strefa.objects.filter(parking__rodzaj_parkingu="krotkoterminowy")


class TicketLongTerm(forms.ModelForm):
    class Meta:
        model = BiletDlugoterminowy
        fields = ['bilet', 'rezerwacjaa']
    
    def __init__(self):
        super(TicketLongTerm, self).__init__()
        self.fields['strefa'].queryset = models.Strefa.objects.filter(parking__rodzaj_parkingu="dlugoterminowy")