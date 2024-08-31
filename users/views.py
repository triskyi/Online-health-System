# users/views.py
from rest_framework import generics
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
import random
from .forms import SignUpForm
from .utils import generate_one_time_code, send_registration_sms
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .utils import send_registration_sms
import random

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import DoctorSerializer
from health_records.models import HealthRecord

from rest_framework import status
from .models import DoctorProfile
from .serializers import DoctorProfileSerializer
from .forms import DoctorProfileForm

from django.views import View
from django.utils.decorators import method_decorator
from django.db import connection
from .models import Appointment, DoctorProfile




class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer



def index(request):
    return render(request, 'users/index.html')  


 
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Get the selected role from the form

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if the user is confirmed
            if not user.is_confirmed:
                messages.error(request, 'Your account is not verified. Please verify your phone number first.')
                return redirect('verify')
            
            # Check if the authenticated user's role matches the selected role
            if user.role == role:
                login(request, user)
                
                if user.role == 'PATIENT':
                    messages.info(request, 'You are logged in as a patient.')
                    return redirect('patient_dashboard')  # Redirect to patient dashboard
                elif user.role == 'DOCTOR':
                    messages.info(request, 'You are logged in as a Doctor.')
                    return redirect('doctor_dashboard')  # Redirect to doctor dashboard
                  
                else:
                    return redirect('index')  # Redirect to home page or another default page
            else:
                # Handle case where role does not match
                messages.error(request, 'Invalid role selection.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login.html')

@login_required
def patient_dashboard_view(request):
    return render(request, 'users/patient_dashboard.html')

@login_required
def patient_dashboard(request):
    user = request.user

    # Check if user has any emergency alerts
    user_has_emergency_alert = HealthRecord.objects.filter(user=user, has_emergency_alert=True).exists()

    return render(request, 'patient_dashboard.html', {
        'user_has_emergency_alert': user_has_emergency_alert
    })  

  
@login_required
def doctor_dashboard_view(request):
    try:
        profile = DoctorProfile.objects.get(doctor=request.user)
    except DoctorProfile.DoesNotExist:
        profile = None
    
    return render(request, 'users/doctor_dashboard.html', {'doctor': profile})




@csrf_exempt
def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_confirmed = False  # Initialize as not confirmed
            user.save()

            # Generate and save verification code
            verification_code = generate_one_time_code()
            user.verification_code = verification_code
            user.save()

            # Send SMS with verification code
            sms_sent = send_registration_sms(user.phone_number, verification_code)

            if sms_sent:
                # Store user ID in session for verification
                request.session['user_id'] = user.id

                # Redirect to verify code page
                messages.success(request, 'Account created successfully! Please verify your account.')
                return redirect('verify')  # Redirect to verification page after successful signup
            else:
                # Handle SMS sending failure
                messages.error(request, 'Failed to send verification code. Please try again.')
        else:
            # Handle invalid form submission
            messages.error(request, 'Invalid form submission. Please correct the errors.')
    else:
        form = SignUpForm()

    return render(request, 'users/sign_up.html', {'form': form})

User = get_user_model()

def verify_code_view(request):
    if request.method == 'POST':
        code_entered = request.POST.get('verification_code')
        user_id = request.session.get('user_id')

        if user_id:
            user = get_object_or_404(CustomUser, id=user_id)

            # Check if the user is a superuser and has not been verified
            if user.is_superuser and not user.is_confirmed:
                if code_entered == user.verification_code:
                    user.is_active = True
                    user.is_confirmed = True
                    user.save()
                    messages.success(request, 'Superuser account confirmed. You can now log in.')
                    return redirect('login')
                else:
                    messages.error(request, 'Invalid verification code. Please try again.')
                    return render(request, 'users/verify.html')

            # For other users or already verified superusers, check the verification code normally
            if code_entered == user.verification_code:
                user.is_active = True
                user.is_confirmed = True
                user.save()
                messages.success(request, 'Account verified successfully! You can now log in.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid verification code. Please try again.')
                return render(request, 'users/verify.html')

        else:
            messages.error(request, 'User ID not found in session. Please sign up again.')

    return render(request, 'users/verify.html')







class ActiveDoctorsView(APIView):
    def get(self, request, *args, **kwargs):
        # Fetching active doctors
        active_doctors = CustomUser.objects.filter(role='DOCTOR', is_active=True)
        serializer = DoctorSerializer(active_doctors, many=True)
        return Response(serializer.data)


def logout_view(request):
    logout(request)
    return redirect('index')  


@method_decorator(login_required, name='dispatch')
class DoctorProfileView(View):
    def get(self, request):
        profile = None

        try:
            profile = DoctorProfile.objects.get(doctor=request.user)
            form = DoctorProfileForm(instance=profile)
        except DoctorProfile.DoesNotExist:
            form = DoctorProfileForm()

        return render(request, 'users/doctor_profile.html', {'form': form, 'doctor': profile})

    def post(self, request):
        if request.user.is_authenticated:
            try:
                profile = DoctorProfile.objects.get(doctor=request.user)
                form = DoctorProfileForm(request.POST, request.FILES, instance=profile)
            except DoctorProfile.DoesNotExist:
                # Create a new profile and assign the doctor field
                form = DoctorProfileForm(request.POST, request.FILES)
                profile = form.save(commit=False)  # Create the form instance without saving to DB
                profile.doctor = request.user  # Assign the current user to the doctor field
                profile.save()  # Now save to the DB
                return redirect('doctor_profile')  # Redirect after creating new profile

            if form.is_valid():
                form.save()
                return redirect('doctor_profile')  # Redirect after updating the profile
        
        return redirect('login')  # If not authenticated, redirect to login


from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from .models import DoctorProfile

@login_required
@require_GET
def available_specialties(request):
    # Fetch all unique specialties from the DoctorProfile model
    specialties = DoctorProfile.objects.values_list('specialty', flat=True).distinct()
    return JsonResponse({'specialties': list(specialties)})

@login_required
@require_GET
def available_doctors(request):
    specialty = request.GET.get('specialty')
    if specialty:
        doctors = DoctorProfile.objects.filter(specialty=specialty).values('id', 'doctor__username')  # Adjust 'doctor__username' to the actual related user field if different
        return JsonResponse({'doctors': list(doctors)})
    return JsonResponse({'doctors': []})

@login_required
@require_GET
def doctor_working_hours(request, doctor_id):
    try:
        doctor = DoctorProfile.objects.get(id=doctor_id)
        working_hours = {
            'work_start_time': doctor.work_start_time.strftime('%H:%M'),
            'work_end_time': doctor.work_end_time.strftime('%H:%M'),
        }
        return JsonResponse({'working_hours': working_hours})
    except DoctorProfile.DoesNotExist:
        return JsonResponse({'working_hours': {}})
@login_required
@require_GET
def doctor_working_days(request, doctor_id):
    try:
        doctor = DoctorProfile.objects.get(id=doctor_id)
        working_days = doctor.working_days.split(',') if doctor.working_days else []
        return JsonResponse({'working_days': working_days})
    except DoctorProfile.DoesNotExist:
        return JsonResponse({'working_days': []})
    

@csrf_exempt
def create_appointment(request):
    if request.method == 'POST':
        # Parse the incoming data
        patient_name = request.POST.get('patientName')
        appointment_date = request.POST.get('appointmentDate')
        specialty = request.POST.get('specialty')
        doctor_id = request.POST.get('doctor')
        working_day = request.POST.get('workingDays')
        appointment_time = request.POST.get('appointmentTime')

        # Retrieve the DoctorProfile instance
        try:
            doctor = DoctorProfile.objects.get(id=doctor_id)
        except DoctorProfile.DoesNotExist:
            return JsonResponse({'error': 'Doctor not found'}, status=404)

        # Create and save a new Appointment instance
        appointment = Appointment(
            patient_name=patient_name,
            appointment_date=appointment_date,
            specialty=specialty,
            doctor=doctor,
            working_day=working_day,
            appointment_time=appointment_time
        )
        appointment.save()

        return redirect('patient_dashboard')

    return redirect('patient_dashboard')


def patient_list_view(request):
    # Query all appointments for the current doctor
    appointments = Appointment.objects.filter(doctor=request.user.doctorprofile)
    return render(request, 'users/patient_list.html', {'appointments': appointments})

def patient_detail_view(request, appointment_id):
    # Get detailed information about the specific appointment
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'users/patient_detail.html', {'appointment': appointment})