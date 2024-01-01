from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('register/',Registration.as_view(),name='register'),
    path('login/',UserLogin.as_view(),name='login'),
    path('logout/',UserLogout.as_view(),name='logout'),
    path('profile/',EditProfile.as_view(),name='profile'),
    path('transfer_money/', TransferMoneyView.as_view(), name='transfer_money'),
    path('change_pass/',ChangePassword, name='change_pass'),
]
