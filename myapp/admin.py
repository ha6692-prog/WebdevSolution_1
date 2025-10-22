from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Appointment, Doctor, Feedback

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_patient', 'is_doctor', 'is_staff')
    list_filter = ('is_patient', 'is_doctor', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_patient', 'is_doctor')}),
    )

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('patient__username', 'doctor__user__username')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'experience', 'available')
    list_filter = ('specialization', 'available')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'message')
