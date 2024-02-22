from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import StudentUser

class StudentUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = StudentUser
        fields = ('username', 'password1', 'password2')
