
from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email=forms.EmailField(required=True)

    def clean_email(self):
        if CustomUser.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('the given email is already registered')
        return self.cleaned_data['email']
    

    class Meta(UserCreationForm):
        model=CustomUser
        fields=('username','email','age','firstname')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model=CustomUser
        fields=('username','email','age','firstname')