from django.urls import path, include
from parking_app import views

app_name='parking_app'
urlpatterns = [
    path('<str:plate_number>', views.new_parking, name='new_parking'),
]