from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=[
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('ADMIN', 'Admin'),
        ('SUPPORT', 'Support Staff'),
        ('PHARMACIST', 'Pharmacist'),
    ])
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new instances
            if self.is_superuser:
                self.is_active = True
                self.is_confirmed = True
        super().save(*args, **kwargs)

class DoctorProfile(models.Model):
    working_days = models.CharField(max_length=255, blank=True, null=True)  # Comma-separated string
    doctor = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    work_start_time = models.TimeField()
    work_end_time = models.TimeField()
    phone_number = models.CharField(max_length=15)
    specialty = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    

    def __str__(self):
        return f"{self.doctor.username}'s Profile"
    

class Appointment(models.Model):
    patient_name = models.CharField(max_length=255)
    appointment_date = models.DateField()
    specialty = models.CharField(max_length=100, blank=True, null=True)  # Changed to CharField
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    working_day = models.CharField(max_length=20)  # E.g., "Monday"
    appointment_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment with {self.doctor.doctor.username} on {self.appointment_date} at {self.appointment_time}"