import pandas as pd
import numpy as np
from django.db import migrations
import os
from django.db import transaction

from . import generate_data as gd

app = 'parking_app'

def update_strefa(apps, schema_editor):
    path = os.path.dirname(os.path.abspath(__file__))
    strefa_updated_df = pd.read_csv(path + '/wygenerowane/strefa_updated.csv')

    Strefa = apps.get_model(app, 'Strefa')       

    for _, row in strefa_updated_df.iterrows():        
        s = Strefa.objects.get(nazwa=row['nazwa'])
        s.liczba_wolnych_miejsc = int(row['liczba_wolnych_miejsc'])
        s.save()


def tests_data_migration(apps, schema_editor):
    path = os.path.dirname(os.path.abspath(__file__))
    # return
    # generator = gd.DataGenerator()
    # generator.generate_data(500)
    # generator.save_data()
    klient_df = pd.read_csv(path + '/wygenerowane/klient.csv')
    migrate_klient(apps, klient_df)
    print('migrate pojazd')
    pojazd_df = pd.read_csv(path + '/wygenerowane/pojazd.csv')
    migrate_pojazd(apps, pojazd_df)
    print('migrate bilet')
    bilet_df = pd.read_csv(path + '/wygenerowane/bilet.csv')
    migrate_bilet(apps, bilet_df)
    print('migrate oplata')
    oplata_df = pd.read_csv(path + '/wygenerowane/oplata.csv')
    migrate_oplata(apps, oplata_df)
    print('migrate rezerwacja')
    rezerwacja_df = pd.read_csv(path + '/wygenerowane/rezerwacja.csv')
    migrate_rezerwacja(apps, rezerwacja_df)
    print('migrate bilet dlugoterminowy')
    bilet_dl_df = pd.read_csv(path + '/wygenerowane/bilet_dlugoterminowy.csv')
    migrate_bilet_dlugoterminowy(apps, bilet_dl_df)
    print('migrate combine rezerwacja and bilet')
    migrate_combine_rezerwacja_and_bilet(apps, rezerwacja_df, bilet_dl_df)
    
def migrate_klient(apps, df):
    Klient = apps.get_model(app, 'Klient')   

    for _, row in df.iterrows():        
        m = Klient(imie=row['imie'], nazwisko=row['nazwisko'], nr_tel=row['nr_telefonu'])
        m.save()

def migrate_pojazd(apps, df):
    Pojazd = apps.get_model(app, 'Pojazd')   
    TypPojazdu = apps.get_model(app, 'TypPojazdu')
    Klient = apps.get_model(app, 'Klient')   

    for _, row in df.iterrows():        
        m = Pojazd(nr_rejestracyjny=row['nr_rejestracyjny'])
        m.typ_pojazdu = TypPojazdu.objects.get(typ=row['typ_pojazdu'])
        #indices from 1
        m.klient = Klient.objects.get(id=int(row['id_klienta'])+1)
        m.save()

def migrate_bilet(apps, df):
    Bilet = apps.get_model(app, 'Bilet')       
    Strefa = apps.get_model(app, 'Strefa')   
    Kara = apps.get_model(app, 'Kara')

    for _, row in df.iterrows():        
        m = Bilet(nr_biletu=row['nr_biletu'], czas_wjazdu=row['czas_wjazdu'],
                  czas_wyjazdu=row['czas_wyjazdu'],
                  wykupiony_czas=row['wykupiony_czas'])
        m.strefa = Strefa.objects.get(id=int(row['id_strefy'])+1)
        m.kara = Kara.objects.get(id=1)
        m.save()

def migrate_oplata(apps, df):
    Oplata = apps.get_model(app, 'Oplata')       
    Bilet = apps.get_model(app, 'Bilet')   
    MetodaPlatnosci = apps.get_model(app, 'MetodaPlatnosci')
    Znizka = apps.get_model(app, 'Znizka')    
    Kara = apps.get_model(app, 'Kara')

    for _, row in df.iterrows():        
        
        m = Oplata(czas=row['czas'], kwota_podstawowa=row['kwota_podstawowa'],
                   kwota_ostateczna=row['kwota_ostateczna'], status=row['status'])
        m.bilet = Bilet.objects.get(id=int(row['id_biletu'])+1)
        m.metoda_platnosci = MetodaPlatnosci.objects.get(rodzaj=row['metoda_platnosci'])

        if not np.isnan(row['id_kary']):
            m.kara = Kara.objects.get(id=int(row['id_kary'])+1)

        if not np.isnan(row['id_znizki']):
            m.znizka = Znizka.objects.get(id=int(row['id_znizki'])+1)
        
        m.save()


def migrate_rezerwacja(apps, df):
    Rezerwacja = apps.get_model(app, 'Rezerwacja')       
    Klient = apps.get_model(app, 'Klient')   
    MiejsceParkingowe = apps.get_model(app, 'MiejsceParkingowe')   

    for _, row in df.iterrows():                
        m = Rezerwacja(nr_rezerwacji=row['nr_rezerwacji'],
                       data_rozpoczecia=row['data_rozpoczecia'],
                       data_zakonczenia=row['data_zakonczenia'])
        m.klient = Klient.objects.get(id=int(row['klient'])+1)        
        m.miejsce_parkingowe = MiejsceParkingowe.objects.get(id=int(row['miejsce_parkingowe'])+1)
        m.save()        

def migrate_bilet_dlugoterminowy(apps, df):
    BiletDlugoterminowy = apps.get_model(app, 'BiletDlugoterminowy')       
    Bilet = apps.get_model(app, 'Bilet')   
    
    for _, row in df.iterrows():                
        m = BiletDlugoterminowy()
        m.bilet = Bilet.objects.get(id=int(row['id_biletu'])+1)        
        m.save()

def migrate_combine_rezerwacja_and_bilet(apps, rezerwacja_df, bilet_df):

    Rezerwacja = apps.get_model(app, 'Rezerwacja')
    BiletDlugoterminowy = apps.get_model(app, 'BiletDlugoterminowy')      

    for index, row in rezerwacja_df.iterrows():                
        m = Rezerwacja.objects.get(id=index+1)
        m.bilet_dlugoterminowy = BiletDlugoterminowy.objects.get(bilet=int(row['bilet_dlugoterminowy'])+1)        
        m.save()

    for index, row in bilet_df.iterrows():                
        m = BiletDlugoterminowy.objects.get(bilet=int(row['id_biletu'])+1)
        m.rezerwacjaa = Rezerwacja.objects.get(id=int(row['id_rezerwacji'])+1)        
        m.save()

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