from django.contrib.auth import authenticate, login, logout
from pyexpat.errors import messages
from datetime import datetime
from datetime import timedelta

from .models import UserProfile, RoomCategory, Bill, Room, Booking
from .forms import CreateUserForm
from django.shortcuts import render, redirect
from django.http import HttpResponse


# For Starter Page
def Start(request):
    params = {'isuserAuth': request.user.is_authenticated}
    userid = request.user.id
    return render(request, 'hotel/home.html', params)


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
    basic_available = 0
    medium_available = 0
    advanced_available = 0

    rooms = Room.objects.filter(room_category_id="basic")
    for room in rooms:
        if (room.is_booked == False):
            basic_available = basic_available + 1

    rooms = Room.objects.filter(room_category_id="medium")
    for room in rooms:
        if (room.is_booked == False):
            medium_available = medium_available + 1

    rooms = Room.objects.filter(room_category_id="advanced")
    for room in rooms:
        if (room.is_booked == False):
            advanced_available = advanced_available + 1

    params = {'basicRoomAvailable': basic_available, 'mediumRoomAvailable': medium_available,
              'advancedRoomAvailable': advanced_available, }
    return render(request, 'hotel/booking.html', params)


def bookingDetails(request, roomType):
    user = UserProfile.objects.get(user_id=request.user.id)
    bookings = Booking.objects.filter(user_id_id=user.id)
    if bookings is not None:
        return HttpResponse("You can't book more than one room")
    room_category = RoomCategory.objects.get(category_name=roomType)
    rooms = Room.objects.filter(room_category_id=roomType)
    room = rooms[0]
    for x in rooms:
        if (x.is_booked != True):
            room = x
            break

    params = {'user': user, 'room': room_category, 'room1': room}

    return render(request, 'hotel/bookingdetails.html', params)


def dashboard(request):
    userid = (request.user.id - 1)
    booking = Booking.objects.get(user_id_id=userid)
    billid = booking.bill_id_id
    bill = Bill.objects.get(id=billid)
    roomid = booking.room_id_id
    room = Room.objects.get(id=roomid)
    roomCategoryid = room.room_category_id
    roomCategory = RoomCategory.objects.get(category_name=roomCategoryid)
    params = {'booking': booking, 'room': room, 'roomCategory': roomCategory, 'bill': bill}
    if (datetime.now() == booking.checkout_time):
        query = f'UPDATE hotel_room SET is_booked = 0 WHERE id = {roomid}'
        room.objects.raw(query)
        return HttpResponse("Your Booking has expired")
    return render(request, 'hotel/dashboard.html', params)


def bookfinal(request, roomType):
    # this peice of code will book the room
    if request.method == 'POST':
        user = UserProfile.objects.get(user_id=request.user.id)
        room_category = RoomCategory.objects.get(category_name=roomType)
        rooms = Room.objects.filter(room_category_id=roomType)
        room = rooms[0]
        for x in rooms:
            if (x.is_booked != True):
                room = x
                break
        bill = Bill()
        bill.user_name = user.fullname
        bill.amount = room_category.price
        bill.transaction_id = request.POST.get('transactionId')
        bill.billing_date = datetime.now()
        bill.save()
        booking = Booking()
        booking.checkin_time = datetime.now()
        # booking.checkout_time = (datetime.now() + timedelta(days=1))
        booking.checkout_time = datetime.now()
        booking.bill_id_id = bill.id
        booking.room_id_id = room.id
        booking.user_id_id = user.id
        booking.save()
        room1 = Room()
        room1.is_booked = True
        room1.id = room.id
        room1.room_category_id = room.room_category_id
        room1.save()
        return render(request, 'hotel/dashboard.html')


def contactus(request):
    return render(request, 'hotel/contactus.html')
