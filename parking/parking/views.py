from django.shortcuts import render, redirect
from users.models import User
from django.contrib.auth.hashers import make_password


def main(request):
    if request.user.is_authenticated:
        return redirect('/parking/add/prices')

    else:
        if not User.objects.exists():
            user = User(username="admin", password=make_password('admin'), is_superuser=True, is_staff=True, is_active=True)
            user.save()

        return render(request, 'main.html')
