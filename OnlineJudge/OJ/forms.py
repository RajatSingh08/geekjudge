from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class UpdateProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'profile_pic']
