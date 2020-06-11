from . import models

def get_db_stats():
    stats = []
    stats.append(("Rezerwacje", models.Rezerwacja.objects.count()))
    stats.append(("Bilety", models.Bilet.objects.count()))
    stats.append(("Klienci", models.Klient.objects.count()))
    stats.append(("Pojazdy", models.Pojazd.objects.count()))
    return {'stats': stats}
