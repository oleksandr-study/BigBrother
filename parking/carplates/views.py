from django.contrib import messages
import glob
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from carplates.forms import imageForm, plateNumberForm
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

            try:
                plate_number = recognition(str(settings.MEDIA_ROOT / 'images/plate.jpg'))
            except:
                return redirect('/carplates/manually')
            if not plate_number:
                message = "Plate number not detected!"

                files = glob.glob(str(settings.MEDIA_ROOT / 'images/*'))
                for file in files:
                    os.remove(file)

                return redirect('/carplate/manually', {'message': message})
            else:
                if not CarPlate.objects.filter(plate_number=plate_number).exists():
                    add_new_carplate(request.user, plate_number)

                else:
                    if CarPlate.objects.get(plate_number=plate_number).banned:
                        message = 'Carplate banned!'

                        files = glob.glob(str(settings.MEDIA_ROOT / 'images/*'))
                        for file in files:
                            os.remove(file)

                        return render(request, 'check-carplate.html', {'message': message})

                files = glob.glob(str(settings.MEDIA_ROOT / 'images/*'))
                for file in files:
                    os.remove(file)

            return redirect(f"/parking/{plate_number}")
    else:
        form = imageForm()

    return render(request, 'check-carplate.html', {'form': form})


@login_required(login_url='/users/login')
def add_carplate_manually(request):
    if request.method == 'POST':
        form = plateNumberForm(request.POST)
        if form.is_valid():
            plate_number = str(form.cleaned_data['plate_number']).replace(' ', '').upper()

            if not plate_number:
                message = "Plate number not detected!"
                form = plateNumberForm()
                return render(request, 'carplate_manual.html', {'form': form, 'message': message})

            if not CarPlate.objects.filter(plate_number=plate_number).exists():
                add_new_carplate(request.user, plate_number)
            else:
                if CarPlate.objects.get(plate_number=plate_number).banned:
                    message = 'Carplate banned'
                    return render(request, 'carplate_manual.html', {'form': form, 'message': message})

            files = glob.glob(str(settings.MEDIA_ROOT / 'images/*'))
            for file in files:
                os.remove(file)

            return redirect(f"/parking/{plate_number}")
    else:
        form = plateNumberForm()
        message = None

    return render(request, 'carplate_manual.html', {'form': form})



def add_new_carplate(user, plate_number):
    carplate = CarPlate()
    carplate.user = user
    carplate.plate_number = plate_number
    carplate.parked_now = False
    carplate.save()
    return carplate.plate_number
