from django import forms
from .models import Bilet, BiletDlugoterminowy
from . import models

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
        fields = ['rezerwacjaa']
    
    def __init__(self, *args, **kwargs):
        super(TicketLongForm, self).__init__(*args, **kwargs)
        self.fields['strefa']=forms.ModelChoiceField(queryset=models.Strefa.objects.filter(parking__rodzaj_parkingu="dlugoterminowy"))