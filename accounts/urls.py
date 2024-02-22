from django.urls import path
from . import views

urlpatterns = [
    
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'), 
    path('logout/', views.user_logout, name='logout'),
    path('profile/',views.profile, name= 'profile'),
    #path('candidates/<str:position>/', views.candidate_list, name='candidate_list'),
   
    #path('insert/', views.insert_usernames, name='insert'),
]
