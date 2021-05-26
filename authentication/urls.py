from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginPage, name='Login'),
    path('LogOut/', views.LogOut, name='LogOut'),
    path('SignUp/', views.SignUpPage, name='SignUp'),
    path('ForgotPassword/', views.ForgotPasswordPage, name='ForgotPassword'),
    path('OTP/', views.OTPPage, name='Otp'),
    path('ResetPassword/', views.ResetPasswordPage, name='ResetPassword'),
]