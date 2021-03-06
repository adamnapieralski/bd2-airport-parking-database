from . import models
import os
from django.conf import settings
from django.http import HttpResponse
from django.apps import apps
import numpy as np
import csv
import datetime

def check_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except(ValueError, TypeError):
        return False

def get_repoting_data(table, date_from, date_to):
    models_names = []
    models_list = apps.get_app_config('parking_app').get_models()
    for model in models_list:
        models_names.append(model._meta.db_table.replace('parking_app_', ''))

    if table is None:
        return {'stats': get_db_stats(), 'tables': models_names, 'data': None}

    model = apps.get_model('parking_app', table)    
    attributes = [f.name for f in model._meta.concrete_fields]           
    
    if table == 'bilet' and check_date(date_from) and check_date(date_to):
        data = model.objects.filter(czas_wjazdu__range=[date_from, date_to]).values_list(*attributes)
    elif table == 'bilet' and check_date(date_from):
        data = model.objects.filter(czas_wjazdu__gte=datetime.datetime.strptime(date_from, '%Y-%m-%d')).values_list(*attributes)
    elif table == 'bilet' and check_date(date_to):
        data = model.objects.filter(czas_wjazdu__lte=datetime.datetime.strptime(date_to, '%Y-%m-%d')).values_list(*attributes)
    else:
        data = model.objects.all().values_list(*attributes)

    attributes = [attr.replace('_', ' ') for attr in attributes]
    data_dict = {'attributes': attributes, 'data': data, 'table': table, 'date_from': date_from, 'date_to': date_to}
    return {'stats': get_db_stats(), 'tables': models_names, 'data': data_dict}   

def get_general_stats():
    general_stats = []
    general_stats.append(("Rezerwacje", models.Rezerwacja.objects.count()))
    general_stats.append(("Bilety", models.Bilet.objects.count()))
    general_stats.append(("Klienci", models.Klient.objects.count()))
    general_stats.append(("Pojazdy", models.Pojazd.objects.count()))
    return general_stats

def get_payment_stats():
    payment_stats = []
    payments = models.Oplata.objects.values_list('kwota_ostateczna', flat=True)
    discounts = models.Oplata.objects.filter(znizka__isnull = False).count()
    penalties = models.Oplata.objects.filter(kara__isnull = False).count()
    sum = 0
    for p in payments:
        sum += p       

    payment_stats.append(("Łączny zysk", round(sum, 2)))
    payment_stats.append(("Liczba przyznanych zniżek", discounts))
    payment_stats.append(("Liczba nałożonych kar", penalties))
    return payment_stats

def get_parking_zone_stats():
    tickets = models.Bilet.objects.values_list('strefa', flat=True)
    values, count = np.unique(np.array(tickets), return_counts=True)
    zone_stats = []
    for i in range(values.size):
        zone_stats.append((models.Strefa.objects.values_list('nazwa', flat=True).get(id=values[i]), count[i]))
    return zone_stats

def get_payment_method_stats():
    payments = models.Oplata.objects.values_list('metoda_platnosci', flat=True)
    values, count = np.unique(np.array(payments), return_counts=True)
    payment_method_stats = []
    for i in range(values.size):
        payment_method_stats.append((values[i], count[i]))
    return payment_method_stats


def get_db_stats():
    return {'general_stats': get_general_stats(), 'payment_stats': get_payment_stats(),
            'zone_stats': get_parking_zone_stats(), 'payment_method_stats': get_payment_method_stats()}


def export_stats_to_csv(type):
    file_name = 'parking_' + type + '.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
    writer = csv.writer(response)

    stats = get_db_stats()
    for row in stats[type]:
        writer.writerow(row)

    return response 

def download_table(table):
    file_name = 'parking_' + table + '.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)

    model = apps.get_model('parking_app', table)    
    attributes = [f.name for f in model._meta.concrete_fields]

    writer = csv.writer(response)
    writer.writerow(attributes)   
    
    items = model.objects.all().values_list(*attributes)

    for item in items:
        writer.writerow(item)    
    return response