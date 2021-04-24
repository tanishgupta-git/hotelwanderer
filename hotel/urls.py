from django.urls import path
from . import views
app_name = 'hotel'
urlpatterns = [
    path('',views.Start, name='start'),
    path('signup/', views.UserRegister, name='signup'),
    path('login/',views.UserLogin,name='login'),
    path('logout/',views.UserLogout,name='logout'),
    path('booking/',views.bookingMenu,name='booking'),
    path('bookingdetails/<roomType>/',views.bookingDetails,name='bookingdetails'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('contactus/',views.contactus,name='contactus'),
    path('bookfinal/<roomType>/',views.bookfinal,name='bookfinal')
]