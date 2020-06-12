from . import models
import os
from django.conf import settings
from django.http import HttpResponse

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

    payment_stats.append(("Łączny zysk", sum))
    payment_stats.append(("Liczba przyznanych zniżek", discounts))
    payment_stats.append(("Liczba nałożonych kar", penalties))

    return {'general_stats': general_stats, 'payment_stats': payment_stats}


def export_stats_to_csv():
    file_path = os.path.join(settings.MEDIA_ROOT, 'parking_stats.csv')
    create_stats_csv(file_path)
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="text/plain")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response

         
def create_stats_csv(file_path):
    stats = get_db_stats()
    with open(file_path, 'w') as f:
        f.write('Statystyki parkingu\n')
        for row in stats['general_stats']:
            f.write(row[0] + ',' + str(row[1]) + '\n')