from django.db import models
from django.contrib.auth.models import AbstractUser
from carplates.models import CarPlate


class Parking(models.Model):
    carplate = models.ForeignKey(CarPlate, on_delete=models.CASCADE)
    parked_at = models.DateTimeField(auto_now_add=True)
    unparked_at = models.DateTimeField(null=True)
    parked_time = models.DurationField(null=True)
    value = models.FloatField(default=0)
    # user = models.ForeignKey(CarUser, on_delete=models.CASCADE)

    def set_parked_time(self):
        self.parked_time = self.unparked_at - self.parked_at

    def __str__(self):
        return self.carplate.plate_number


class ParkingPrice(models.Model):
    duration_from = models.DurationField()
    duration_to = models.DurationField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

