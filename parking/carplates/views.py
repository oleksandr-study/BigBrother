from django.shortcuts import render, redirect
from carplates.forms import imageForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def upload_picture(request):
    if request.method == 'POST':
        form = imageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT / 'images')
            filename = fs.save(image.name, image)
            return redirect('users:profile')
    else:
        form = imageForm()
    return render(request, 'upload-picture.html', {'form': form})
