from datetime import datetime

from django.shortcuts import render
from parking_app.models import Parking
from carplates.models import CarPlate

# Create your views here.
def new_parking(request, plate_number):
    carplate = CarPlate.objects.get(plate_number=plate_number)
    if carplate.parked_now:
        carplate.parked_now = False
        parking = Parking.objects.filter(carplate=carplate).order_by('-parked_at').first()
        parking.unparked_at = datetime.now()
        parking.set_parked_time()
        parking.save()

        duration = parking.parked_time


        message = f'Парковка закінчилася в {parking.unparked_at}'

    else:
        parking = Parking()
        parking.carplate = carplate
        parking.parked_at = datetime.now()
        parking.save()

