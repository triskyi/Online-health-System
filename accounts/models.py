from django.db import models
from django.contrib.auth.models import AbstractUser





class StudentUser(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=False)
    phone = models.CharField(max_length=25)
    vote = models.IntegerField(default=0)
    profile_updated = models.BooleanField(default=False) 
    is_candidate = models.BooleanField(default=False)
    groups = models.ManyToManyField('auth.Group', related_name='student_users')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='student_user_permissions')

    def __str__(self):
        return self.username



