from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('vote/<int:candidate_id>/', views.vote, name='vote'),
  
]
