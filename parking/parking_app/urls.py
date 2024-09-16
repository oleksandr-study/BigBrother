from django.urls import path, include
from parking_app import views

app_name='parking_app'
urlpatterns = [
    path('<str:plate_number>', views.new_parking, name='new_parking'),
    path('export/csv', views.export_csv, name='export_csv'),
    path('add-prices', views.create_prices, name='create_prices')
]