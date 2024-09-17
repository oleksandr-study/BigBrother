from datetime import timedelta

import csv
from django.shortcuts import render, redirect
from parking_app.models import Parking, ParkingPrice
from carplates.models import CarPlate
from django.http import HttpResponse
from io import StringIO
import numpy as np
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required(login_url='/users/login')
def new_parking(request, plate_number):
    carplate = CarPlate.objects.get(plate_number=plate_number)
    if carplate.parked_now:
        carplate.parked_now = False
        carplate.save()
        parking = Parking.objects.filter(carplate=carplate).order_by('-parked_at').first()
        parking.unparked_at = timezone.now()
        parking.save()
        parking.parked_time = timezone.now() - parking.parked_at
        parking.save()

        parking_price = ParkingPrice.objects.filter(duration_from__lte=parking.parked_time,
                                                    duration_to__gte=parking.parked_time).first()
        parking.value = parking_price.price * (parking.parked_time.seconds // 60)
        parking.save()
        message = f"Парковка закінчилася в {parking.unparked_at.time().strftime('%H:%M:%S')}"

    else:
        parking = Parking()
        parking.carplate = carplate
        carplate.parked_now = True
        parking.parked_at = timezone.now()
        carplate.save()
        parking.save()

        message = f"Парковка почалася в {parking.parked_at.time().strftime('%H:%M:%S')}"

    return render(request, 'add_parking.html', {'plate_number': plate_number, 'message': message})


@login_required(login_url='/users/login')
@login_required(login_url='/users/login')
def export_csv(request):
    user = request.user
    parkings = Parking.objects.select_related('carplate').filter(carplate__user=user)

    if not parkings.exists():
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Немає даних для експорту'])
        output.seek(0)
        response = HttpResponse(output, content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="parking_data.csv"'
        return response

    data = []
    for parking in parkings:
        plate_number = parking.carplate.plate_number
        parked_at = parking.parked_at.strftime('%Y-%m-%d %H:%M') if parking.parked_at else ''
        unparked_at = parking.unparked_at.strftime('%Y-%m-%d %H:%M') if parking.unparked_at else ''
        parked_time = parking.parked_time.total_seconds() if parking.parked_time else 0
        value = parking.value
        data.append([plate_number, parked_at, unparked_at, parked_time, value])

    np_data = np.array(data)

    parked_times = np_data[:, 3].astype(float)
    values = np_data[:, 4].astype(float)

    total_parked_time = np.sum(parked_times)
    total_value = np.sum(values)

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Номер платіжки', 'Час паркування', 'Час виїзду', 'Час паркування (секунди)', 'Вартість'])
    writer.writerows(np_data)
    writer.writerow(['Всього', '', '', f'{total_parked_time / 3600:.2f} годин', f'{total_value:.2f}'])
    
    output.seek(0)
    response = HttpResponse(output, content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="parking_data.csv"'

    return response

@login_required(login_url='/users/login')
def create_prices(request):
    if ParkingPrice.objects.exists():
        return redirect('/carplates')
    else:
        prices = [
            {"duration_from": timedelta(minutes=0), "duration_to": timedelta(minutes=30), "price": 0.00},
            {"duration_from": timedelta(minutes=31), "duration_to": timedelta(minutes=60), "price": 2.00},
            {"duration_from": timedelta(minutes=61), "duration_to": timedelta(minutes=120), "price": 1.50},
            {"duration_from": timedelta(minutes=121), "duration_to": timedelta(minutes=300), "price": 1.20},
            {"duration_from": timedelta(minutes=301), "duration_to": timedelta(minutes=99999), "price": 1.00},
        ]

        for price_data in prices:
            ParkingPrice.objects.create(
                duration_from=price_data["duration_from"],
                duration_to=price_data["duration_to"],
                price=price_data["price"]
            )
        return redirect('/carplates')
