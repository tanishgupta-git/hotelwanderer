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