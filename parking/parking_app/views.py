from datetime import datetime

from django.shortcuts import render
from parking_app.models import Parking, ParkingPrice
from carplates.models import CarPlate

# Create your views here.
def new_parking(request, plate_number):
    carplate = CarPlate.objects.get(plate_number=plate_number)
    if carplate.parked_now:
        carplate.parked_now = False
        parking = Parking.objects.filter(carplate=carplate).order_by('-parked_at').first()
        parking.unparked_at = datetime.now()
        parking.set_parked_time()

        duration = parking.parked_time.seconds // 60
        price = ParkingPrice.objects.filter(duration_from__lte=duration, duration_to__gte=duration).first()
        parking.value = price.price
        parking.save()

        message = f'Парковка закінчилася в {parking.unparked_at}'

    else:
        parking = Parking()
        parking.carplate = carplate
        parking.parked_at = datetime.now()
        parking.save()

        message = f"Парковка почалася в {parking.parked_at}"

    return render(request, 'add_parking.html', {'plate_number': plate_number, 'message': message})