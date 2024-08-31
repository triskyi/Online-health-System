# Generated by Django 5.0.4 on 2024-08-25 12:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_start_time', models.TimeField()),
                ('work_end_time', models.TimeField()),
                ('phone_number', models.CharField(max_length=15)),
                ('specialty', models.CharField(blank=True, max_length=100, null=True)),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]