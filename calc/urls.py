from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Use a unique name, e.g., 'home'
    path('add', views.add, name='add'),
]
