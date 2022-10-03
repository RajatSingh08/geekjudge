from django import forms
from django.forms import ModelForm
from USERS.models import Submission

class CodeForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['user_code']
        widgets = {'user_code' : forms.Textarea()}