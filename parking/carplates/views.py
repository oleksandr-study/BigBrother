from django.contrib import messages
import glob
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from carplates.forms import imageForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from carplates.models import CarPlate
from carplates.recognition import recognition


@login_required(login_url='/users/login')
def check_carplate(request):
    if request.method == 'POST':
        form = imageForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.cleaned_data['image']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT / 'images')
            fs.save('plate.jpg', image)

            plate_number = recognition(str(settings.MEDIA_ROOT / 'images/plate.jpg'))
            if not plate_number:
                message = "Plate number not detected!"
                form = imageForm()
                return render(request, 'check-carplate.html', {'form': form, 'message': message})
            else:
                if not CarPlate.objects.filter(plate_number=plate_number).exists():
                    add_new_carplate(request.user ,plate_number)

                else:
                    if CarPlate.objects.get(plate_number=plate_number).banned:
                        messages.error(request, 'Carplate banned')
                        return render(request, 'check-carplate.html', {'form': form})

                files = glob.glob(str(settings.MEDIA_ROOT / 'images/*'))
                for file in files:
                    os.remove(file)

            return redirect(f"/parking/{plate_number}")
    else:
        form = imageForm()
    return render(request, 'check-carplate.html', {'form': form})


def add_new_carplate(user, plate_number):
    carplate = CarPlate()
    carplate.user = user
    carplate.plate_number = plate_number
    carplate.parked_now = False
    carplate.save()
    return carplate.plate_number
