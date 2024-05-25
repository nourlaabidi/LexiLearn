# audio_app/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('record/', record_audio, name='record_audio'),
    path('listen/', listen_audio, name='listen_audio'),
    #path('evaluation/', evaluation, name='evaluation'),
    #path('evaluation/', evaluate_audio, name='evaluation'),
    path('evaluation/', save_audio, name='save_audio'),
    #path('evaluate_audio/', evaluate_audio, name='evaluate_audio'),
    path('evaluation/<int:audio_id>/', evaluate_page, name='evaluate_page'),
]
