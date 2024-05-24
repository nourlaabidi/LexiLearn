from django.urls import path
from main import admin
from . import views
urlpatterns = [
    path('welcomeO/', views.welcomeO, name="welcomeO"),
    path('welcomeC/', views.welcomeC, name="welcomeC"),
    path('loginPage/', views.loginPage, name="loginPage"),
    path('loginPageChild/', views.loginPageChild, name="loginPageChild"),
    path('registerOrthophoniste/', views.registerOrthophoniste, name="registerOrthophoniste"),
    path('logout/', views.logoutPage, name="logout"),
    path('', views.home, name="home"),
    path('createChild/', views.create_child, name="createChild"),
    path('delete_child/', views.DeleteChild, name='DeleteChild'),
    path('search_child/', views.searchUser, name='searchUser'),
    path('test/', views.test, name='test'),
    path('accounts/', views.accounts, name='accounts'),
    
    
]