# health_records/urls.py

from django.urls import path
from .views import reception_view

urlpatterns = [
    path('reception/', reception_view, name='reception_view'),
    # Add other health record URL patterns as needed
]
