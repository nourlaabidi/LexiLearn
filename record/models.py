# audio_app/models.py

from django.db import models

class AudioFile(models.Model):
    name = models.CharField(max_length=100)
    audio_id=models.IntegerField(unique=True,null=True)
    audio = models.FileField(upload_to='audio/')
    score=models.IntegerField(null=True)

    
class Word(models.Model):
    word_id=models.IntegerField(unique=True,null=True)
    word=models.CharField(max_length=20,null=True)
    audio=models.FileField(upload_to='audio/')