
from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import CustomUser,Profile


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder':'Username',
                                                             'class':'form-control',
                                                             }))
    def clean_username(self):
        if CustomUser.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError('Username exists')
        return self.cleaned_data['username']
    
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder':'Username',
                                                           'class':'form-control',
                                                           }))

    def clean_email(self):
        if CustomUser.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('the given email is already registered')
        return self.cleaned_data['email']
    
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder':'Password',
                                                                  'class':'form-control',
                                                                  'data-toggle':'password',
                                                                  'id':'password',
                                                                  }))

    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password',
                                                                  'class':'form-control',
                                                                  'data-toggle':'password',
                                                                  'id':'password'}))
    
    class Meta:
        model=CustomUser
        fields=['username','email','password1','password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'pUsername',
                                                             'class': 'form-control',
                                                             }))
    
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name' : 'password',
                                                                 }))
    
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username','password','remember_me']

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control',}))
    
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = CustomUser
        fields = ['username','email']

class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    social_media = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar','social_media','full_name','bio']

