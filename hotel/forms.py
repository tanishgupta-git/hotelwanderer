from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class CreateUserForm(UserCreationForm):
    password =  forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)
    fullame = forms.CharField(max_length=250, required=True)
    email = forms.CharField(max_length=250, required=True)
    aadharid = forms.CharField(max_length=250, required=True)
    mobilenumber = forms.CharField(max_length=10, required=True)
    permanentaddress = forms.CharField(max_length=250, required=True)
    class Meta:
        model = User
        fields = ['username','fullame','email','aadharid','mobilenumber','permanentaddress','password','password1']