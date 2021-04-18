from django.urls import path
from . import views
app_name = 'hotel'
urlpatterns = [
    path('',views.Start, name='start'),
    path('signup/', views.UserRegister, name='signup'),
    path('login/',views.UserLogin,name='login'),
    path('logout/',views.UserLogout,name='logout'),
]