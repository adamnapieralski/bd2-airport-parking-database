from . import models
import os
from django.conf import settings
from django.http import HttpResponse
from django.apps import apps
import csv

def get_repoting_data():
    models_names = []
    models_list = apps.get_app_config('parking_app').get_models()
    for model in models_list:
        models_names.append(model._meta.db_table.replace('parking_app_', ''))

    return {'stats': get_db_stats(), 'tables': models_names}

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
    file_path = os.path.join(settings.MEDIA_ROOT, 'parking_stats.csv')
    create_stats_csv(file_path, type)
    download_file(file_path)
         
def create_stats_csv(file_path, type):
    stats = get_db_stats()
    with open(file_path, 'w') as f:
        f.write('Statystyki parkingu\n')
        for row in stats[type]:
            f.write(row[0] + ',' + str(row[1]) + '\n')

def download_table(table):
    file_name = 'parking_' + table + '.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)

    model = apps.get_model('parking_app', table)
    # attributes = [f.name for f in model._meta.get_fields(include_parents=False, include_hidden=False)]
    attributes = [f.name for f in model._meta.concrete_fields]

    writer = csv.writer(response)
    writer.writerow(attributes)   
    
    items = model.objects.all().values_list(*attributes)

    for item in items:
        writer.writerow(item)    
    return response

def create_table_csv(table):
    stats = get_db_stats()
    with open(file_path, 'w') as f:
        f.write('Statystyki parkingu\n')
        for row in stats[type]:
            f.write(row[0] + ',' + str(row[1]) + '\n')


def download_file(file_path):
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="text/plain")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response