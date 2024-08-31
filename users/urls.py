from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    UserListCreateView,
    login_view,
    index,
    sign_up_view,
    verify_code_view,
    logout_view,
    patient_dashboard_view,
    doctor_dashboard_view,
    ActiveDoctorsView,
    DoctorProfileView,
    available_specialties, available_doctors, doctor_working_hours,doctor_working_days,create_appointment,patient_list_view, patient_detail_view
)

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('login/', login_view, name='login'),
    path('patient/', patient_dashboard_view, name='patient_dashboard'),
    path('doctor/', doctor_dashboard_view, name='doctor_dashboard'),
    path('api/active-doctors/', ActiveDoctorsView.as_view(), name='active-doctors'),
    path('doctor-profile/', DoctorProfileView.as_view(), name='doctor_profile'),  # Changed to 'doctor_profile'
    path('sign_up/', sign_up_view, name='sign_up'),
    path('verify/', verify_code_view, name='verify'),
    path('', index, name='index'),
    path('logout/', logout_view, name='logout'),
    path('api/available-specialties/', available_specialties, name='available_specialties'),
    path('api/available-doctors/', available_doctors, name='available_doctors'),
    path('api/doctor-working-hours/<int:doctor_id>/', doctor_working_hours, name='doctor_working_hours'),
    path('doctor/<int:doctor_id>/working-days/', doctor_working_days, name='doctor_working_days'),
    path('api/create-appointment/', create_appointment, name='create_appointment'),
    path('patients/', patient_list_view, name='patient_list'),
    path('patients/<int:appointment_id>/', patient_detail_view, name='patient_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
