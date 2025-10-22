from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, AppointmentForm, FeedbackForm, UserForm, LoginForm
from .models import Appointment, User, Doctor, Feedback
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

# Home View
def home(request):
    return render(request, 'home.html')

# Login View
@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('appointments')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

# Register View
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Don't login automatically, redirect to login page instead
            messages.success(request, 'Registration successful! Please log in to continue.')
            return redirect('login')  # Redirect to login page after registration
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

# Appointments View
@login_required
def appointments(request):
    user_appointments = Appointment.objects.filter(patient=request.user)
    context = {
        'appointments': user_appointments
    }
    return render(request, 'appointments.html', context)

# Create Appointment View
@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            messages.success(request, 'Appointment created successfully!')
            return redirect('appointments')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AppointmentForm()

    return render(request, 'create_appointment.html', {'form': form})

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
