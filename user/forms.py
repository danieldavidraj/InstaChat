from django import forms
from .models import UserProfile

class UserRegistrationForm(forms.ModelForm):
    Email=forms.EmailField()
    UserID=forms.CharField(max_length=30)
    Password=forms.CharField(widget = forms.PasswordInput())
    RetypePassword=forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model=UserProfile
        fields=['UserID','Email','Password']

class UserLoginForm(forms.Form):
    UserID=forms.CharField(max_length=30)
    Password=forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model=UserProfile
        fields=['UserID','Password']

class ForgotPasswordForm(forms.Form):
    Email = forms.EmailField()
    class Meta:
        model=UserProfile
        fields=['Email']

class OTPForm(forms.Form):
    Otp=forms.CharField(max_length=4)

class ResetPasswordForm(forms.Form):
    newPassword=forms.CharField(widget = forms.PasswordInput())
    reTypeNewPassword=forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model=UserProfile
        fields=['Email','Password']

