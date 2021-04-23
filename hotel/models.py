from django.db import models    
from django.contrib.auth.models import Permission, User

class UserProfile(models.Model):
    user = models.ForeignKey(User,models.SET_NULL,blank=True,null=True)
    fullname = models.CharField(max_length=250) 
    email = models.CharField(max_length=250)
    aadharid = models.CharField(max_length=100)
    mobilenumber = models.IntegerField()
    permanentaddress = models.CharField(max_length=250)

    def __str__(self):
        return self.fullname

class RoomCategory(models.Model):
    category_name = models.CharField(max_length=250,primary_key=True)
    price = models.FloatField(max_length=10)
    gym = models.BooleanField()
    balcony = models.BooleanField()
    wifi = models.BooleanField()
    ac = models.BooleanField()

    def __str__(self):
        return self.category_name

class Bill(models.Model):
    transaction_id = models.CharField(max_length=250)
    amount = models.FloatField(max_length=10)
    user_name = models.CharField(max_length=250)
    billing_date = models.DateTimeField()

class Room(models.Model):
    is_booked = models.BooleanField()
    room_category = models.ForeignKey(RoomCategory,models.DO_NOTHING)

class Booking(models.Model):
    user_id = models.ForeignKey(User,models.DO_NOTHING)
    room_id = models.ForeignKey(Room,models.DO_NOTHING)
    bill_id = models.ForeignKey(Bill,models.DO_NOTHING)
    checkin_time = models.DateTimeField()
    checkout_time = models.DateTimeField()