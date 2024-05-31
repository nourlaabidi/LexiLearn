from datetime import date
from django.contrib.auth.models import User, AbstractUser
from django.db import models

class Group(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owned_group')
    members = models.ManyToManyField(User, related_name='group_membership', blank=True, default=None )
    
    def __str__(self):
        return f"Groupe {self.id} - Propriétaire: {self.owner.username}"

class AudioFile(models.Model):
    name = models.CharField(max_length=100)
    audio_id=models.IntegerField(unique=True,null=True)
    audio = models.FileField(upload_to='audio/')
    score=models.IntegerField(null=True)

    
class Word(models.Model):
    word = models.CharField(max_length=20, null=True)
    level = models.IntegerField(null=True)
    
    def __str__(self):
        return f"{self.word}"

class Child(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='child')
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}"

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

class Exercise(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    words = models.ManyToManyField(Word)

    def __str__(self):
        return f"Exercise for {self.child.user.username}"

    