from django.contrib import admin
from .models import Parking

@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ['carplate', 'parked_at', 'unparked_at', 'value']
    search_fields = ['carplate__plate_number']
