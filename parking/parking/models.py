from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    def __str__(self):
        return self.username


class CarPlate(models.Model):
    plate_number = models.CharField(max_length=20, unique=True)
    parking_status = models.BooleanField(default=False)
    parking_count = models.IntegerField(default=0)
    banned = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.plate_number


class Parking(models.Model):
    car_plate = models.ForeignKey(CarPlate, on_delete=models.CASCADE)
    parking_start = models.DateTimeField(default=datetime.now)
    parking_end = models.DateTimeField()
    parking_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

