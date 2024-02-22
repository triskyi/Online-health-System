# accounts/admin.py
from django.contrib import admin
from .models import StudentUser
from django.contrib.auth.admin import UserAdmin

from .forms import StudentUserCreationForm

class CustomStudentUserAdmin(UserAdmin):
    add_form = StudentUserCreationForm
admin.site.register(StudentUser, CustomStudentUserAdmin)

