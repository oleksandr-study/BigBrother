from django.contrib import admin
from .models import CarPlate

@admin.register(CarPlate)
class CarPlateAdmin(admin.ModelAdmin):
    list_display = ['plate_number', 'user', 'parking_count', 'parked_now', 'banned']
    list_filter = ['banned', 'parked_now', 'user']
    search_fields = ['plate_number']
    actions = ['ban_car', 'unban_car']
    fields = ['plate_number', 'user', 'parking_count', 'parked_now', 'banned']

    def ban_car(self, request, queryset):
        queryset.update(banned=True)
    ban_car.short_description = 'Ban selected cars'

    def unban_car(self, request, queryset):
        queryset.update(banned=False)
    unban_car.short_description = 'Unban selected cars'