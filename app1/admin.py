from django.contrib import admin
from .models import User, Doctor, Appointment, Feedback

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_doctor', 'is_patient')
    list_filter = ('is_doctor', 'is_patient', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'experience', 'available')
    list_filter = ('specialization', 'available')
    search_fields = ('user__username', 'user__email', 'specialization')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'doctor__specialization')
    search_fields = ('patient__username', 'doctor__user__username', 'reason')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'comments')
