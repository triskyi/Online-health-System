# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import DoctorProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    phone_number = forms.CharField(max_length=15, help_text='Required')
    role = forms.ChoiceField(choices=[
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('ADMIN', 'Admin'),
        ('SUPPORT', 'Support Staff'),
        ('PHARMACIST', 'Pharmacist'),
    ], help_text='Required')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'role', 'password1', 'password2')
class VerificationForm(forms.Form):
    verification_code = forms.CharField(label='Verification Code', max_length=6)




class DoctorProfileForm(forms.ModelForm):
    WORKING_DAYS_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    SPECIALTY_CHOICES = [
        ('cardiologist', 'Cardiologist'),
        ('neurologist', 'Neurologist'),
        ('orthopedic_surgeon', 'Orthopedic Surgeon'),
        ('pediatrician', 'Pediatrician'),
        ('oncologist', 'Oncologist'),
        # Add more specializations as needed
    ]

    working_days = forms.MultipleChoiceField(
        choices=WORKING_DAYS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    
    specialty = forms.ChoiceField(
        choices=SPECIALTY_CHOICES,
        widget=forms.Select,
        required=True,
    )

    class Meta:
        model = DoctorProfile
        fields = ['specialty', 'working_days', 'work_start_time', 'work_end_time', 'phone_number', 'image']
        widgets = {
            'work_start_time': forms.TimeInput(attrs={'type': 'time'}),
            'work_end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_working_days(self):
        days = self.cleaned_data.get('working_days', [])
        return ','.join(days)  # Convert list to comma-separated string

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.working_days = self.cleaned_data.get('working_days', '')
        if commit:
            instance.save()
        return instance
    

# forms.py
from django import forms
from .models import Appointment, DoctorProfile

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'appointment_date', 'specialty', 'doctor', 'working_day', 'appointment_time']

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        # Customize form fields if necessary, for example, populate doctors based on a condition
        self.fields['doctor'].queryset = DoctorProfile.objects.filter(active=True)  # Example condition
