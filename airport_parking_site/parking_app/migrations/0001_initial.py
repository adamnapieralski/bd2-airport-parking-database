# Generated by Django 3.0.5 on 2020-04-28 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingLot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('zones_amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ParkingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('duration', models.DurationField()),
                ('parking_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.ParkingType')),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('capacity', models.IntegerField()),
                ('free_spaces', models.IntegerField()),
                ('parking_lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.ParkingLot')),
                ('tarrif', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.Tariff')),
            ],
        ),
        migrations.CreateModel(
            name='ParkingSpace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.Zone')),
            ],
        ),
        migrations.AddField(
            model_name='parkinglot',
            name='parking_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.ParkingType'),
        ),
    ]