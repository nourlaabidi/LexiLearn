# audio_app/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('record/<int:word_id>/', record_audio, name='record_audio'),
    path('home/', home_page, name='home_page'),
    path('listen/', listen_audio, name='listen_audio'),
    path('evaluation/', save_audio, name='save_audio'),
    path('list/', list_words, name='list_words'),
    path('evaluation/<int:audio_id>/', evaluate_page, name='evaluate_page'),
    
]
