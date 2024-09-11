from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)
from django.urls import path, reverse_lazy
from . import views

app_name = "users"

urlpatterns = [
    path('signup/', views.signupuser, name='signup'),  
    path('login/', views.loginuser, name='login'),       
    path('logout/', views.logoutuser, name='logout'),   
    path('profile/', views.profile, name='profile'),  

    # Сброс пароля
    path('reset-password/', 
         views.ResetPasswordView.as_view(), 
         name='password_reset'),
    
    path('reset-password/done/', 
         PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             success_url=reverse_lazy('users:password_reset_complete')
         ), 
         name='password_reset_confirm'),

    path('reset-password/complete/', 
         PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ), 
         name='password_reset_complete'),

]
