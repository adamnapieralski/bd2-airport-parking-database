from django.db import models


class Strefa(models.Model):
    nazwa = models.CharField(max_length=100)
    pojemnosc = models.IntegerField()
    liczba_wolnych_miejsc = models.IntegerField()

    cennik = models.ForeignKey(
        'Cennik',
        on_delete=models.CASCADE,
    )

    parking = models.ForeignKey(
        'Parking',
        on_delete=models.CASCADE,
    )

    typ_pojazdu = models.ForeignKey(
        'TypPojazdu',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.nazwa


class Cennik(models.Model):
    oplata = models.DecimalField(max_digits=7, decimal_places=2)
    czas = models.IntegerField()

    rodzaj_parkingu = models.ForeignKey(
        'RodzajParkingu',
        on_delete=models.CASCADE,
    )


class Parking(models.Model):
    nazwa = models.CharField(max_length=100)
    liczba_stref = models.IntegerField()

    rodzaj_parkingu = models.ForeignKey(
        'RodzajParkingu',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.nazwa


class RodzajParkingu(models.Model):
    rodzaj = models.CharField(primary_key=True, max_length=20)

    def __str__(self):
        return self.rodzaj


class MiejsceParkingowe(models.Model):
    nr_miejsca = models.IntegerField()

    strefa = models.ForeignKey(
        'Strefa',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.nr_miejsca)


class TypPojazdu(models.Model):
    typ = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.typ


class Pojazd(models.Model):
    nr_rejestracyjny = models.CharField(primary_key=True, max_length=10)

    typ_pojazdu = models.ForeignKey(
        'TypPojazdu',
        on_delete=models.CASCADE,
    )

    klient = models.ForeignKey(
        'Klient',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.nr_rejestracyjny


class Rezerwacja(models.Model):
    nr_rezerwacji = models.IntegerField()
    data_rozpoczecia = models.DateTimeField('%Y-%m-%d')  # '2006-10-25'
    data_zakonczenia = models.DateTimeField('%Y-%m-%d')

    klient = models.ForeignKey(
        'Klient',
        on_delete=models.CASCADE,
    )

    miejsce_parkingowe = models.ForeignKey(
        'MiejsceParkingowe',
        on_delete=models.CASCADE,
    )

    bilet_dlugoterminowy = models.ForeignKey(
        'BiletDlugoterminowy',
        on_delete=models.CASCADE,
        related_name='+',
    )

    def __str__(self):
        return str(self.nr_rezerwacji)


class Bilet(models.Model):
    nr_biletu = models.IntegerField()
    czas_wjazdu = models.TimeField('%H:%M')  # '14:30'
    czas_wyjazdu = models.TimeField('%H:%M')
    wykupiony_czas = models.IntegerField()

    strefa = models.ForeignKey(
        'Strefa',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.nr_biletu)


class Klient(models.Model):
    imie = models.CharField(max_length=200)
    nazwisko = models.CharField(max_length=300)
    nr_tel = models.IntegerField()

    def __str__(self):
        return self.imie + "_" + self.nazwisko


class BiletDlugoterminowy(models.Model):
    id_biletu = models.OneToOneField(
        'Bilet',
        on_delete=models.CASCADE,
        primary_key=True,
    )

    rezerwacja = models.ForeignKey(
        'Rezerwacja',
        on_delete=models.CASCADE,
    )
