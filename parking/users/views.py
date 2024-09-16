from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import HttpResponse

from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile, User


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
        return redirect('/')

    form = LoginForm()
    return render(request, 'users/login.html', context={"form": form})


@login_required(login_url='/users/login')
def logoutuser(request):
    logout(request)
    return redirect(to='users:login')


@login_required(login_url='/users/login')
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

    return render(request, 'users/profile.html', {'profile_form': profile_form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'
