from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Appointments
    path('appointments/', views.appointments, name='appointments'),
    path('create-appointment/', views.create_appointment, name='create_appointment'),
    path('appointments/<int:appointment_id>/update/', views.update_appointment, name='update_appointment'),
    path('appointments/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),

    # Feedback
    path('feedback/', views.submit_feedback, name='feedback'),

    # User profile
    path('profile/', views.user_profile, name='profile'),

    # Doctor dashboard
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/profile/', views.doctor_profile, name='doctor_profile'),
    path('doctor/profile/update/', views.update_doctor_profile, name='update_doctor_profile'),
]