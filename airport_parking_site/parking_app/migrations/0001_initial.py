# Generated by Django 3.0.5 on 2020-06-18 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bilet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nr_biletu', models.IntegerField()),
                ('czas_wjazdu', models.DateTimeField(verbose_name='%Y-%m-%d %H:%M:%S')),
                ('czas_wyjazdu', models.DateTimeField(null=True, verbose_name='%Y-%m-%d %H:%M:%S')),
                ('wykupiony_czas', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Cennik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oplata', models.DecimalField(decimal_places=2, max_digits=7)),
                ('czas', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Kara',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=50)),
                ('wartosc', models.FloatField()),
                ('opis', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Klient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imie', models.CharField(max_length=200)),
                ('nazwisko', models.CharField(max_length=300)),
                ('nr_tel', models.IntegerField()),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MetodaPlatnosci',
            fields=[
                ('rodzaj', models.CharField(max_length=40, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=100)),
                ('liczba_stref', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RodzajParkingu',
            fields=[
                ('rodzaj', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='TypPojazdu',
            fields=[
                ('typ', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Znizka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=50)),
                ('wartosc', models.FloatField()),
                ('opis', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='BiletDlugoterminowy',
            fields=[
                ('bilet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='parking_app.Bilet')),
            ],
        ),
        migrations.CreateModel(
            name='Strefa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=100)),
                ('pojemnosc', models.IntegerField()),
                ('liczba_wolnych_miejsc', models.IntegerField()),
                ('cennik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.Cennik')),
                ('parking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.Parking')),
                ('typ_pojazdu', models.ForeignKey(db_column='typ_pojazdu_typ', on_delete=django.db.models.deletion.CASCADE, to='parking_app.TypPojazdu')),
            ],
        ),
        migrations.CreateModel(
            name='Pojazd',
            fields=[
                ('nr_rejestracyjny', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('klient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.Klient')),
                ('typ_pojazdu', models.ForeignKey(db_column='typ_pojazdu_typ', on_delete=django.db.models.deletion.CASCADE, to='parking_app.TypPojazdu')),
            ],
        ),
        migrations.AddField(
            model_name='parking',
            name='rodzaj_parkingu',
            field=models.ForeignKey(db_column='rodzaj_parkingu_rodzaj', on_delete=django.db.models.deletion.CASCADE, to='parking_app.RodzajParkingu'),
        ),
        migrations.CreateModel(
            name='Oplata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('czas', models.DateTimeField(verbose_name='%Y-%m-%d %H:%M:%S')),
                ('kwota_podstawowa', models.FloatField()),
                ('kwota_ostateczna', models.FloatField()),
                ('status', models.CharField(max_length=1)),
                ('bilet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.Bilet')),
                ('kara', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parking_app.Kara')),
                ('metoda_platnosci', models.ForeignKey(db_column='metoda_platnosci_rodzaj', on_delete=django.db.models.deletion.CASCADE, to='parking_app.MetodaPlatnosci')),
                ('znizka', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parking_app.Znizka')),
            ],
        ),
        migrations.CreateModel(
            name='MiejsceParkingowe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nr_miejsca', models.IntegerField()),
                ('strefa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.Strefa')),
            ],
        ),
        migrations.AddField(
            model_name='cennik',
            name='rodzaj_parkingu',
            field=models.ForeignKey(db_column='rodzaj_parkingu_rodzaj', on_delete=django.db.models.deletion.CASCADE, to='parking_app.RodzajParkingu'),
        ),
        migrations.AddField(
            model_name='bilet',
            name='strefa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.Strefa'),
        ),
        migrations.CreateModel(
            name='Rezerwacja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nr_rezerwacji', models.IntegerField()),
                ('data_rozpoczecia', models.DateTimeField(verbose_name='%Y-%m-%d')),
                ('data_zakonczenia', models.DateTimeField(verbose_name='%Y-%m-%d')),
                ('klient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.Klient')),
                ('miejsce_parkingowe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.MiejsceParkingowe')),
                ('bilet_dlugoterminowy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='parking_app.BiletDlugoterminowy')),
            ],
        ),
        migrations.AddField(
            model_name='biletdlugoterminowy',
            name='rezerwacjaa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parking_app.Rezerwacja'),
        ),
    ]
