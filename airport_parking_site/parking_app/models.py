from django.db import models

class Zone(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    free_spaces = models.IntegerField()

    tarrif = models.ForeignKey(
        'Tariff',
        on_delete=models.CASCADE,
    )

    parking_lot = models.ForeignKey(
        'ParkingLot',
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return self.name

class Tariff(models.Model):
    price = models.DecimalField(max_digits=7, decimal_places=2)
    duration = models.IntegerField()
    parking_type = models.ForeignKey(
        'ParkingType',
        on_delete=models.CASCADE,
    )

class ParkingLot(models.Model):
    name = models.CharField(max_length=100)
    zones_amount = models.IntegerField()
    parking_type = models.ForeignKey(
        'ParkingType',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class ParkingType(models.Model):
    p_type = models.CharField(max_length=20)

    def __str__(self):
        return self.p_type

class ParkingSpace(models.Model):
    number = models.IntegerField()
    zone = models.ForeignKey(
        'Zone',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.number)

