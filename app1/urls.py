from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('appointments/', views.appointments, name='appointments'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/update/<int:appointment_id>/', views.update_appointment, name='update_appointment'),
    path('appointments/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('feedback/', views.feedback, name='feedback'),
    path('profile/', views.user_profile, name='profile'),
    path('doctor/profile/', views.doctor_profile, name='doctor_profile'),
    path('doctor/profile/update/', views.update_doctor_profile, name='update_doctor_profile'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
]
