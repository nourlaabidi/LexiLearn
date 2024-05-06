from django.urls import path
from main import admin
from . import views
urlpatterns = [
    path('welcomePage/', views.welcomePage, name="welcomePage"),
    path('loginOrthophoniste/', views.loginOrthophoniste, name="loginOrthophoniste"),
    path('registerOrthophoniste/', views.registerOrthophoniste, name="registerOrthophoniste"),
    path('loginPatient/', views.loginPatient, name="loginPatient"),
    path('logout/', views.logoutPage, name="logout"),
    path('', views.home, name="home"),
    
    
]