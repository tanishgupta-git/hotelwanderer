from django.contrib.auth import authenticate, login,logout
from .models import UserProfile
from .forms import CreateUserForm
from django.shortcuts import render
from django.http import HttpResponse


# For Login Form Page
def UserLogin(request):
    if request.user.is_authenticated:
        return redirect('hotel:start')
    else:       
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('hotel:start')
            else:
                messages.info(request,'Username or Password is incorrect')

        return render(request,'hotel/login.html')


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
            if form.is_valid():
                user = form.save(commit=False)
                password = form.cleaned_data["password"]
                password1 = form.cleaned_data["password1"]
                fullname = form.cleaned_data["fullname"]
                email = form.cleaned_data["email"]
                adharid = form.cleaned_data["adharid"]
                mobilenumber = form.cleaned_data["mobilenumber"] 
                permanentaddress = form.changed_data["permanentaddress"]
                if password == password1:
                    user.set_password(password)
                    user.save()
                    userprofile = UserProfile()
                    userprofile.user = user
                    userprofile.fullname = fullname
                    userprofile.email = email
                    userprofile.aadharid = adharid
                    userprofile.mobilenumber = mobilenumber
                    userprofile.permanentaddress = permanentaddress
                    userprofile.save()
                    messages.success(request,"Account created successfully " )
                    return redirect('hotel:login')
                else:
                    messages.success(request,"Password Doesn't Match")
        else:
            return render(request,'hotel/registration.html',{form:form})