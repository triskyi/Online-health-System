# users/serializers.py
from rest_framework import serializers
from .models import CustomUser
from .utils import send_registration_sms
from django.contrib.auth.password_validation import validate_password
from .models import DoctorProfile


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'date_of_birth', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
            date_of_birth=validated_data.get('date_of_birth'),
            phone_number=validated_data.get('phone_number'),
        )
        user.set_password(validated_data['password'])
        user.save()
        # Send one-time SMS here
        send_registration_sms(user.phone_number)
        return user


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']  # Adjust fields as necessary
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['id', 'doctor', 'specialty', 'phone_number', 'work_start_time', 'work_end_time', 'image', 'working_days']


# Serializer for CustomUser model
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']  # Adjust fields as necessary

# Serializer for DoctorProfile model
class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['id', 'doctor', 'specialty', 'phone_number', 'work_start_time', 'work_end_time', 'image' ]
