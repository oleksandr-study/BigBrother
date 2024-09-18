from django.urls import path
import carplates.views as views

app_name = 'carplates'

urlpatterns = [
    path('', views.check_carplate, name='check_carplate'),
    path('manually', views.add_carplate_manually, name='add_carplate_manually'),
]