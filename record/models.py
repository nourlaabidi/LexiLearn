# audio_app/models.py
from datetime import date
import os
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from gtts import gTTS

from record_vocal import settings

class AudioFile(models.Model):
    name = models.CharField(max_length=100)
    audio_id=models.IntegerField(unique=True,null=True)
    audio = models.FileField(upload_to='audio/')
    score=models.IntegerField(null=True)


class Group(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owned_group')
    members = models.ManyToManyField(User, related_name='group_membership', blank=True, default=None )
    
    def __str__(self):
        return f"Groupe {self.id} - Propriétaire: {self.owner.username}"
class Child(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='child')
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return f" {self.user.username}"
    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
class AudioFile(models.Model):
    name = models.CharField(max_length=100)
    audio_id=models.IntegerField(unique=True,null=True)
    audio = models.FileField(upload_to='audio/')
    score=models.IntegerField(null=True)

    
class Word(models.Model):
    word=models.CharField(max_length=20,null=True)
    word_vocal= models.FileField(upload_to='recordings/',null=True)
    level=models.IntegerField(null=True)
    def __str__(self):
        return f" {self.word} "
    def prepareAudio(self):
        language = 'en'
        print("My Text:", self.word)
        output = gTTS(text=self.word, lang=language, slow=False)
        file_name = f'{self.id}_output.wav'
        file_path = os.path.join(settings.MEDIA_ROOT, 'recordings', file_name)
        print("File path:", file_path)
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            output.save(file_path)
            print("Audio has been saved at:", file_path)
            self.word_vocal.name = os.path.join('recordings', file_name)
            self.save()
            return file_path
        except Exception as e:
            print("Error saving audio file:", str(e))
            return None