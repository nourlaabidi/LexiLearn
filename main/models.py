from datetime import date
from django.contrib.auth.models import User, AbstractUser
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
    
    
    

    

    