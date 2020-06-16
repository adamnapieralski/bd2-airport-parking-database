from . import models
import os
from django.conf import settings
from django.http import HttpResponse
from django.apps import apps

def get_data():
    strefy_names = []
    strefy = models.Strefa.objects.all()
    for strefa in strefy:
        strefy_names.append(strefa.nazwa)

    return {'strefy_names': strefy_names}

def calculate_paid_time(cennik, kwota):
    paid_time = 0
    paid_time_value = 0
    for c in cennik:
        if c.czas < 0:
            while paid_time_value + c.oplata <= kwota:
                paid_time_value += c.oplata
                paid_time += 1
            break
        if c.oplata <= kwota:
            paid_time = c.czas
            paid_time_value = c.oplata
        else:
            break
    return paid_time

def calculate_min_pay_price(cennik, czas_do_oplaty):
    price = 0
    for c in cennik:
        if c.czas < 0:
            wykupiony_czas = -c.czas
            while czas_do_oplaty > wykupiony_czas:
                wykupiony_czas += 1
                price += c.oplata
            break
        price = c.oplata
        if czas_do_oplaty <= c.czas:
            break
    return price
        