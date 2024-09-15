from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile, User
from carplates.models import CarPlate
from parking_app.models import Parking

def signupuser(request):
    if request.user.is_authenticated:
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
        else:
            return render(request, 'users/signup.html', context={'form': form})
        
    return render(request, 'users/signup.html', context={'form': RegisterForm()})

def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to='users:profile')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return render(request, 'users/login.html', context={"form": form})

        login(request, user)
        return redirect(to='users:profile')

    form = LoginForm()  
    return render(request, 'users/login.html', context={"form": form})

@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='users:login')

@login_required
def profile(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users:profile')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    
    car_plates = CarPlate.objects.filter(user=request.user)
    parking_history = Parking.objects.filter(carplate__in=car_plates)
    
    context = {
        'profile_form': profile_form,
        'car_plates': car_plates,
        'parking_history': parking_history,
    }
    
    return render(request, 'users/profile.html', context)

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'
