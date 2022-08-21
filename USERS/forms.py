from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from .models import User

import email
from enum import unique


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(label='Email',widget=forms.TextInput(attrs={"placeholder":"Email","id":"email"})) 
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class UpdateProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'profile_pic']
