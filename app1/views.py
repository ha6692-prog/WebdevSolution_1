from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (CustomUserCreationForm, AppointmentForm, FeedbackForm, CustomLoginForm, 
                    UserForm, MultiStepRegistrationForm, DateSelectionForm, ReasonForm,
                    DoctorSelectionForm, AppointmentTypeForm, TimeSlotForm)
from .models import Appointment, User, Doctor, Feedback, AVAILABLE_TIME_SLOTS
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.views import LoginView

# Home View
def home(request):
    return render(request, 'home.html')

# Custom Login View
class LoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Login successful!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('home')

# Register View
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = MultiStepRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, f'Registration successful! Welcome {user.first_name}. Please log in to continue.')
                return redirect('login')  # Redirect to login page after registration
            except Exception as e:
                messages.error(request, f'An error occurred during registration: {str(e)}')
        else:
            # If form is invalid, show errors
            messages.error(request, 'Please correct the errors below.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = MultiStepRegistrationForm()

    return render(request, 'register.html', {'form': form})

# Appointments View
@login_required
def appointments(request):
    if request.method == 'POST':
        # Handle appointment booking
        try:
            doctor_id = request.POST.get('doctor')
            appointment_type = request.POST.get('appointment_type')
            appointment_date = request.POST.get('appointment_date')
            time_slot = request.POST.get('time_slot')
            reason = request.POST.get('appointment_reason', '')
            
            # Get the doctor object
            doctor = Doctor.objects.get(user_id=doctor_id)
            
            # Parse the time slot
            # Time can be in either "HH:MM AM/PM" or "HH:MM" format
            from datetime import datetime
            try:
                # Try 12-hour format first (e.g., "09:00 AM")
                time_obj = datetime.strptime(time_slot, "%I:%M %p").time()
            except ValueError:
                # Try 24-hour format (e.g., "09:00")
                time_obj = datetime.strptime(time_slot, "%H:%M").time()
            
            # Create the appointment
            appointment = Appointment.objects.create(
                patient=request.user,
                doctor=doctor,
                appointment_type=appointment_type,
                date=appointment_date,
                time=time_obj,
                reason=reason,
                status='pending'
            )
            
            messages.success(request, 'Appointment booked successfully! You will receive a confirmation email shortly.')
            # After successful booking, redirect to the booked confirmation page
            return redirect('book_appointment')
            
        except Doctor.DoesNotExist:
            messages.error(request, 'Selected doctor not found.')
        except Exception as e:
            messages.error(request, f'An error occurred while booking the appointment: {str(e)}')
    
    # GET request - display the form
    user_appointments = Appointment.objects.filter(patient=request.user)
    doctors = Doctor.objects.all().select_related('user')
    
    # Create forms for Crispy Forms integration
    doctor_form = DoctorSelectionForm(doctors=doctors)
    appointment_type_form = AppointmentTypeForm()
    date_form = DateSelectionForm()
    
    # Get time slots from models constant and format for display
    time_slots = [display for value, display in AVAILABLE_TIME_SLOTS]
    time_slot_form = TimeSlotForm(time_slots=time_slots)
    reason_form = ReasonForm()
    
    # Format doctor data for the template
    doctors_data = []
    for doctor in doctors:
        # Get first letter of first and last name for avatar
        first_initial = doctor.user.first_name[0].upper() if doctor.user.first_name else 'D'
        last_initial = doctor.user.last_name[0].upper() if doctor.user.last_name else 'R'
        avatar = f"{first_initial}{last_initial}"
        
        doctors_data.append({
            'id': doctor.pk,
            'name': f"Dr. {doctor.user.get_full_name() or doctor.user.username}",
            'specialty': doctor.specialization,
            'experience': f"{doctor.experience} years",
            'rating': float(doctor.rating),
            'consultationFee': float(doctor.consultation_fee),
            'available': doctor.available,
            'avatar': avatar,
            'bio': doctor.bio or ''
        })
    
    context = {
        'appointments': user_appointments,
        'doctors': doctors,
        'doctors_data': doctors_data,
        'doctor_form': doctor_form,
        'appointment_type_form': appointment_type_form,
        'date_form': date_form,
        'time_slot_form': time_slot_form,
        'reason_form': reason_form,
    }
    return render(request, 'appointments.html', context)


# Simple view to show booked appointment confirmation / booking details page
@login_required
def book_appointment(request):
    # This page shows a confirmation / detailed booking page after a successful booking.
    # You can enhance it to show the latest booking details if desired.
    return render(request, 'book_appointment.html')

# Note: appointment creation is handled via the multi-step `appointments` view above.
# The separate `create_appointment` view was removed to avoid duplicate/unused code.

# Update Appointment View
@login_required
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully!')
            return redirect('appointments')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'update_appointment.html', {'form': form})

# Cancel Appointment View
@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)

    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment canceled successfully!')
        return redirect('appointments')

    return render(request, 'cancel_appointment.html', {'appointment': appointment})

# Feedback View
@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeedbackForm()

    return render(request, 'submit_feedback.html', {'form': form})

# User Profile View
@login_required
def user_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserForm(instance=user)

    return render(request, 'user_profile.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

# Doctor Profile View
@login_required
def doctor_profile(request):
    if not request.user.is_doctor:
        messages.error(request, 'Access denied. Doctor only.')
        return redirect('home')

    try:
        doctor_profile = request.user.doctor_profile
    except Doctor.DoesNotExist:
        # Create a doctor profile if it doesn't exist
        doctor_profile = Doctor.objects.create(user=request.user, specialization="General", experience=0)

    return render(request, 'doctor_profile.html', {'doctor_profile': doctor_profile})

# Update Doctor Profile View
@login_required
def update_doctor_profile(request):
    if not request.user.is_doctor:
        messages.error(request, 'Access denied. Doctor only.')
        return redirect('home')

    try:
        doctor_profile = request.user.doctor_profile
    except Doctor.DoesNotExist:
        doctor_profile = Doctor.objects.create(user=request.user, specialization="General", experience=0)

    if request.method == 'POST':
        specialization = request.POST.get('specialization')
        experience = request.POST.get('experience')
        available = request.POST.get('available') == 'on'

        if specialization and experience:
            doctor_profile.specialization = specialization
            doctor_profile.experience = experience
            doctor_profile.available = available
            doctor_profile.save()
            messages.success(request, 'Doctor profile updated successfully!')
            return redirect('doctor_profile')
        else:
            messages.error(request, 'Please fill in all required fields.')

    return render(request, 'update_doctor_profile.html', {'doctor_profile': doctor_profile})

# Doctor Dashboard View (for URL consistency)
@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor:
        messages.error(request, 'Access denied. Doctor only.')
        return redirect('home')

    try:
        doctor_profile = request.user.doctor_profile
    except Doctor.DoesNotExist:
        doctor_profile = Doctor.objects.create(user=request.user, specialization="General", experience=0)

    # Get appointments for this doctor
    doctor_appointments = Appointment.objects.filter(doctor=doctor_profile).order_by('-date')

    context = {
        'doctor_profile': doctor_profile,
        'appointments': doctor_appointments
    }
    return render(request, 'doctor_dashboard.html', context)

# Feedback Page View
def feedback(request):
    return render(request, 'feedback.html')
