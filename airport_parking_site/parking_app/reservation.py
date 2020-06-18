# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 20:15:54 2020

@author: Marcin
"""

from .models import Rezerwacja
from .models import MiejsceParkingowe
from .models import Strefa


def check_reservation(data_rozp,data_zak,typ_pojazdu_sz):
   # zajete_miejsca=Rezerwacja.objects.exclude(data_zakonczenia=data_zak).filter(data_rozpoczecia=data_rozp)
   #Sample.objects.filter(date__range=["2011-01-01", "2011-01-31"])
   rezerwacja_zajete=(Rezerwacja.objects.filter(data_rozpoczecia__range=[data_rozp,data_zak]))
   zajete_miejsca=rezerwacja_zajete.values_list('miejsce_parkingowe')
   strefy=Strefa.objects.filter(typ_pojazdu=typ_pojazdu_sz)
   wolne_miejsca=MiejsceParkingowe.objects.exclude(id=zajete_miejsca.values_list('id')).filter(strefa=strefy[0]).first()
   print(wolne_miejsca)
   return wolne_miejsca
    