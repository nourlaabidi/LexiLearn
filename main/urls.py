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
    path('exercicesChild/', views.exercicesChild, name="exercicesChild"),
    path('delete_child/', views.DeleteChild, name='DeleteChild'),
    path('search_child/', views.searchUser, name='searchUser'),
    path('test/', views.test, name='test'),
    path('accounts/', views.accounts, name='accounts'),
    path('record/', views.record_audio, name='record_audio'),
    path('listen/', views.listen_audio, name='listen_audio'),
    path('evaluation/', views.save_audio, name='save_audio'),
    path('evaluation/<int:audio_id>/', views.evaluate_page, name='evaluate_page'),
    path('select-words/', views.select_words, name='select_words'),
    path('profile/', views.profile, name='profile'),
    path('profileO/', views.profileO, name='profileO'),
    
]