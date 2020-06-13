from . import models
import os
from django.conf import settings
from django.http import HttpResponse
from django.apps import apps
import csv

def get_repoting_data(table):
    models_names = []
    models_list = apps.get_app_config('parking_app').get_models()
    for model in models_list:
        models_names.append(model._meta.db_table.replace('parking_app_', ''))

    if table is None:
        return {'stats': get_db_stats(), 'tables': models_names, 'data': None}

    model = apps.get_model('parking_app', table)    
    attributes = [f.name for f in model._meta.concrete_fields]           
    data = model.objects.all().values_list(*attributes)
    data_dict = {'attributes': attributes, 'data': data}
    return {'stats': get_db_stats(), 'tables': models_names, 'data': data_dict}   

def get_db_stats():
    general_stats = []
    general_stats.append(("Rezerwacje", models.Rezerwacja.objects.count()))
    general_stats.append(("Bilety", models.Bilet.objects.count()))
    general_stats.append(("Klienci", models.Klient.objects.count()))
    general_stats.append(("Pojazdy", models.Pojazd.objects.count()))

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

    return {'general_stats': general_stats, 'payment_stats': payment_stats}


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