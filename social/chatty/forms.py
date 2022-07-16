from django.contrib.auth.models import User
from django import forms
from .models import *

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder' : 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Last Name'}))

    class Meta:
        model = AppUser
        fields = ('first_name', 'last_name')

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'rows' : 6, 'cols' : 35, 'placeholder' : 'Say something...'
    }))

    class Meta:
        model = Post
        fields = ('content', 'image')

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ('first_name', 'last_name', 'pfp')