from django.contrib.auth import authenticate, login, logout
from pyexpat.errors import messages

from .models import UserProfile
from .forms import CreateUserForm
from django.shortcuts import render, redirect
from django.http import HttpResponse


# For Starter Page
def Start(request):
    return render(request, 'hotel/home.html')


# For Login Form Page
def UserLogin(request):
    if request.user.is_authenticated:
        return redirect('hotel:start')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                userdata = UserProfile.objects.get(user=user)
                print(userdata)
                return redirect('hotel:start')
            else:
                messages.info(request, 'Username or Password is incorrect')

        return render(request, 'hotel/login.html')


#  Logout function
def UserLogout(request):
    logout(request)
    return redirect('hotel:login')


# For User Authentication
def UserRegister(request):
    if request.user.is_authenticated:
        return redirect('hotel:start')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            print(form.is_valid())
            if form.is_valid():
                user = form.save(commit=False)
                password1 = form.cleaned_data["password1"]
                password2 = form.cleaned_data["password2"]
                fullname = form.cleaned_data["fullname"]
                email = form.cleaned_data["email"]
                adharid = form.cleaned_data["adharid"]
                mobilenumber = form.cleaned_data["mobilenumber"]
                permanentaddress = form.cleaned_data["permanentaddress"]
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    userprofile = UserProfile()
                    userprofile.user = user
                    userprofile.fullname = fullname
                    userprofile.email = email
                    userprofile.aadharid = adharid
                    userprofile.mobilenumber = mobilenumber
                    userprofile.permanentaddress = permanentaddress
                    userprofile.save()
                    print(userprofile)
                    return redirect('hotel:login')
                else:
                    messages.success(request, "Password Doesn't Match")
            else:
                return render(request, 'hotel/signup.html', {form: form})
        else:
            return render(request, 'hotel/signup.html', {form: form})


def bookingMenu(request):
    params = {'basicRoomAvailable':10,'mediumRoomAvailable':10,'advancedRoomAvailable':10}
    return render(request,'hotel/booking.html',params)


def bookingDetails(request):
    return render(request,'hotel/bookingdetails.html')