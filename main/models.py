from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
'''class Orthophoniste(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    # Modifier les related_name pour éviter les conflits
    groups = models.ManyToManyField(Group, related_name='orthophoniste_set', blank=True, verbose_name=('groups'), help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),)
    user_permissions = models.ManyToManyField(Permission, related_name='orthophoniste_set', blank=True, verbose_name=('user permissions'), help_text=('Specific permissions for this user.'),)

class Patient(AbstractUser):
    # Modifier les related_name pour éviter les conflits
    groups = models.ManyToManyField(Group, related_name='patient_set', blank=True, verbose_name=('groups'), help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),)
    user_permissions = models.ManyToManyField(Permission, related_name='patient_set', blank=True, verbose_name=('user permissions'), help_text=('Specific permissions for this user.'),)'''
