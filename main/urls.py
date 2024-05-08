from django.urls import path
from main import admin
from . import views
urlpatterns = [
    path('welcomeO/', views.welcomeO, name="welcomeO"),
    path('welcomeC/', views.welcomeC, name="welcomeC"),
    path('loginPage/', views.loginPage, name="loginPage"),
    path('registerOrthophoniste/', views.registerOrthophoniste, name="registerOrthophoniste"),
    path('logout/', views.logoutPage, name="logout"),
    path('', views.home, name="home"),
    path('OrthophonistePage/', views.OrthophonistePage, name="OrthophonistePage"),
    path('createChild/', views.create_child, name="createChild"),
    
    
]