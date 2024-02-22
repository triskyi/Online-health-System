

from django.db.models import Q 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import StudentUser     
from django.core.exceptions import ValidationError     
from django.http import HttpResponse



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('student_id')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Please provide both student ID and password.')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, 'Logged in successfully !!!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid student ID or password.')

    return render(request, 'login.html')





def register(request):
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['student_id']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if a user with the same username already exists
        existing_user = StudentUser.objects.filter(username=username).first()

        if existing_user:

            if not StudentUser.objects.filter(email=email).exists():
                # Update the user's profile since they exist and the email is not registered
                existing_user.email = email
                existing_user.phone = phone
                existing_user.first_name = first_name
                existing_user.last_name = last_name
                existing_user.profile_updated = True  # Set the flag to True
                existing_user.set_password(password)  # Update the password if needed
                existing_user.save()
                messages.success(request, 'Profile updated successfully.')
            else:
                # Email is already registered, so no database update is allowed
                messages.error(request, 'Email is already registered.')
        else:
            if not StudentUser.objects.filter(username=username).exists():
                # User is not in the database
                messages.error(request, 'You are not a registered student.')
            elif StudentUser.objects.filter(email=email).exists():
                # Email is already registered
                messages.error(request, 'Email is already registered.')
            elif password == confirm_password:
                user = StudentUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    profile_updated=True  # Set the flag to True for a new user
                )
                # Automatically log in the user after successful registration
                
                login (request, user)
                messages.success(request, 'Registration successful.')
                return render(request, 'login.html')
            else:
                messages.error(request, 'Passwords do not match.')

        return render(request, 'register.html')  # Redirect to the home page

    return render(request, 'register.html')

    




def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('/')  # Redirect to a suitable page after logout





def profile(request):
    return render(request, 'profile.html')
    