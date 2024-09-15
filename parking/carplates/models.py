from django.db import models
from users.models import User


class CarPlate(models.Model):
    plate_number = models.CharField(max_length=10)
    parking_count = models.IntegerField(default=0)
    parked_now = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def str(self):
        return self.plate_number


class ParkingPrice(models.Model):
    duration_from = models.DurationField()
    duration_to = models.DurationField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
