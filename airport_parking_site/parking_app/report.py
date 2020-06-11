from . import models
import os
from django.conf import settings
from django.http import HttpResponse

def get_db_stats():
    stats = []
    stats.append(("Rezerwacje", models.Rezerwacja.objects.count()))
    stats.append(("Bilety", models.Bilet.objects.count()))
    stats.append(("Klienci", models.Klient.objects.count()))
    stats.append(("Pojazdy", models.Pojazd.objects.count()))
    return {'stats': stats}


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
        for row in stats['stats']:
            f.write(row[0] + ',' + str(row[1]) + '\n')