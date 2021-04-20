from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class CreateUserForm(UserCreationForm):
    fullname = forms.CharField(max_length=250, required=True)
    email = forms.CharField(max_length=250, required=True)
    adharid = forms.CharField(max_length=250, required=True)
    mobilenumber = forms.CharField(max_length=10, required=True)
    permanentaddress = forms.CharField(max_length=250, required=True)
    class Meta:
        model = User
        fields = ['username','fullname','email','adharid','mobilenumber','permanentaddress','password1','password2']