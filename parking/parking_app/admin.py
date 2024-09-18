from django.contrib import admin
from .models import Parking, ParkingPrice

@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ['carplate', 'parked_at', 'unparked_at', 'value']
    search_fields = ['carplate__plate_number']


@admin.register(ParkingPrice)
class ParkingPriceAdmin(admin.ModelAdmin):
    list_display = ['duration_from', 'duration_to', 'price']
    search_fields = ['price']