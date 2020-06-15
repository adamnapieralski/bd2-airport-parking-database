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
        fields = []
    
    def __init__(self, *args, **kwargs):
        super(TicketLongForm, self).__init__(*args, **kwargs)
        self.fields['strefa']=forms.ModelChoiceField(queryset=models.Strefa.objects.filter(parking__rodzaj_parkingu="dlugoterminowy"))

    def clean_rezerwacja_id(self):
        rezerwacja_id = self.cleaned_data.get('rezerwacja_id')
        
        if not models.Rezerwacja.objects.filter(id=rezerwacja_id).exists():
            raise forms.ValidationError("Rezerwacja o podanym ID nie istnieje.")

        return rezerwacja_id

    def clean_strefa(self):
        rezerwacja_id = self.cleaned_data.get('rezerwacja_id')
        strefa = self.cleaned_data.get('strefa')

        if not models.Rezerwacja.objects.filter(id=rezerwacja_id, miejsce_parkingowe__strefa=strefa).exists():
            print(models.Rezerwacja.objects.filter(id=rezerwacja_id).values('miejsce_parkingowe__strefa'), strefa)
            raise forms.ValidationError("Ta rezerwacja obowiązuje na innej strefie.")

        return strefa
