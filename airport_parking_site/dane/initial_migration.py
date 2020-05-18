import pandas as pd
from django.db import migrations

from . import generate_data as gd

app = 'parking_app'

def initial_migration(apps, schema_editor):
    # migrate_cennik(apps)
    # migrate_kara(apps)
    # migrate_rodzaj_parkingu(apps)
    # migrate_metoda_platnosci(apps)
    # migrate_typ_pojazdu(apps)
    # migrate_parking(apps)        
    # migrate_strefa(apps)    
    # migrate_znizka(apps)
    migrate_miejsce_parkingowe(apps)
    

def migrate_cennik(apps):
    Cennik = apps.get_model(app, 'Cennik')
    RodzajParkingu = apps.get_model(app, 'RodzajParkingu')
    df = gd.get_cennik_df()

    for _, row in df.iterrows():        
        m = Cennik(oplata=row['oplata'], czas=row['czas'])
        m.rodzaj_parkingu=RodzajParkingu.objects.get(rodzaj=row['rodzaj_parkingu'])
        m.save()

def migrate_kara(apps):
    Kara = apps.get_model(app, 'Kara')
    df = gd.get_kara_df()

    for _, row in df.iterrows():
        m = Kara(nazwa=row['nazwa'], wartosc=row['wartosc'], opis=row['opis'])
        m.save()

def migrate_metoda_platnosci(apps):
    MetodaPlatnosci = apps.get_model(app, 'MetodaPlatnosci')
    df = gd.get_metoda_platnosci_df()

    for _, row in df.iterrows():
        m = MetodaPlatnosci(rodzaj=row['rodzaj'])
        m.save()


def migrate_rodzaj_parkingu(apps):
    RodzajParkingu = apps.get_model(app, 'RodzajParkingu')
    df = gd.get_rodzaj_parkingu_df()

    for _, row in df.iterrows():
        m = RodzajParkingu(rodzaj=row['rodzaj'])
        m.save()

def migrate_parking(apps):
    Parking = apps.get_model(app, 'Parking')
    RodzajParkingu = apps.get_model(app, 'RodzajParkingu')
    df = gd.get_parking_df()

    for _, row in df.iterrows():
        m = Parking(nazwa=row['nazwa'], liczba_stref=row['liczba_stref'])
        m.rodzaj_parkingu=RodzajParkingu.objects.get(rodzaj=row['rodzaj_parkingu'])
        m.save()

def migrate_typ_pojazdu(apps):
    TypPojazdu = apps.get_model(app, 'TypPojazdu')
    df = gd.get_typ_pojazdu_df()

    for _, row in df.iterrows():
        m = TypPojazdu(typ=row['typ'])
        m.save()

def migrate_strefa(apps):
    Strefa = apps.get_model(app, 'Strefa')
    Parking = apps.get_model(app, 'Parking')
    Cennik = apps.get_model(app, 'Cennik')
    TypPojazdu = apps.get_model(app, 'TypPojazdu')

    df = gd.get_strefa_df()

    for _, row in df.iterrows():
        m = Strefa(nazwa=row['nazwa'], pojemnosc=row['pojemnosc'],
                   liczba_wolnych_miejsc=row['liczba_wolnych_miejsc'])
        #indices in db start from 1
        m.parking=Parking.objects.get(id=int(row['id_parkingu']+1))
        m.cennik=Cennik.objects.get(id=int(row['id_cennika']))
        m.typ_pojazdu=TypPojazdu.objects.get(typ=row['typ_pojazdu'])
        m.save()

def migrate_znizka(apps):
    Znizka = apps.get_model(app, 'Znizka')
    df = gd.get_znizka_df()

    for _, row in df.iterrows():
        m = Znizka(nazwa=row['nazwa'], wartosc=row['wartosc'], opis=row['opis'])
        m.save()

def migrate_miejsce_parkingowe(apps):
    MiejsceParkingowe = apps.get_model(app, 'MiejsceParkingowe')
    Strefa = apps.get_model(app, 'Strefa')
    df = gd.get_miejsce_parkingowe_df()

    for _, row in df.iterrows():
        m = MiejsceParkingowe(nr_miejsca=row['nr_miejsca'])
        m.strefa = Strefa.objects.get(id=int(row['strefa'])+1)
        m.save()