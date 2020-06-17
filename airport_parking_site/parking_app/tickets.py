# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 20:15:54 2020

@author: Marcin
"""

from .models import Rezerwacja
from .models import MiejsceParkingowe


def check_reservation(data_rozp,data_zak):
   # zajete_miejsca=Rezerwacja.objects.exclude(data_zakonczenia=data_zak).filter(data_rozpoczecia=data_rozp)
   #Sample.objects.filter(date__range=["2011-01-01", "2011-01-31"])
   zajete_miejsca=MiejsceParkingowe.objects.filter(date__range=[data_rozp,data_zak]) 
   wolne_miejsca=MiejsceParkingowe.objects.exclude(id=zajete_miejsca.id)
   return wolne_miejsca.first()
    