from django.urls import path
import carplates.views as views

app_name = 'carplates'

urlpatterns = [
    path('upload-picture', views.upload_picture, name='upload_picture'),
]