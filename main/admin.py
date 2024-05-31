from django.contrib import admin
from .models import Group, Child, Word, Exercise

admin.site.register(Group)
admin.site.register(Child)
admin.site.register(Word)
admin.site.register(Exercise)
# Register your models here.
