# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 20:15:54 2020

@author: Marcin
"""

from . import models
import os
from django.conf import settings
from django.http import HttpResponse
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass


def check_reservation():
    data=[]
    return True

# def get_data():
#     data = []
#     data.append(("Rezerwacje", models.Klient.imie)))
#     data.append(("Bilety", models.Bilet.objects.count()))
#     data.append(("Klienci", models.Klient.objects.count()))
#     data.append(("Pojazdy", models.Pojazd.objects.count()))
#     return {'data': data}