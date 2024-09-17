from django.db import models
from carplates.models import CarPlate
from decimal import Decimal


class Parking(models.Model):
    carplate = models.ForeignKey(CarPlate, on_delete=models.CASCADE)
    parked_at = models.DateTimeField(auto_now_add=True)
    unparked_at = models.DateTimeField(null=True)
    parked_time = models.DurationField(null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    # user = models.ForeignKey(CarUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.parked_at and self.unparked_at:
            self.parked_time = self.unparked_at - self.parked_at
        super().save(*args, **kwargs)

    def formatted_parked_time(self):
        if self.parked_time is None:
            return ''
        total_seconds = self.parked_time.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

    def __str__(self):
        return self.carplate.plate_number


class ParkingPrice(models.Model):
    duration_from = models.DurationField()
    duration_to = models.DurationField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

