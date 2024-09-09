from django.contrib.auth.models import AbstractUser
from django.db import models
from users.models import User as CarUser  # TODO: змінити назву і чи взагалі юзер треба в цьому файлі
from carplates.models import CarPlate


class User(AbstractUser):
    def __str__(self):
        return self.username


class Parking(models.Model):
    carplate = models.ForeignKey(CarPlate, on_delete=models.CASCADE)
    parked_at = models.DateTimeField(auto_now_add=True)
    unparked_at = models.DateTimeField()
    parked_time = models.TimeField()
    value = models.FloatField(default=0)
    user = models.ForeignKey(CarUser, on_delete=models.CASCADE)

    def set_parked_time(self):
        self.parked_time = self.unparked_at - self.parked_at

    def __str__(self):
        return self.carplate.plate_number
