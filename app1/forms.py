from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Appointment, Feedback, Doctor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML

class DoctorSelectionForm(forms.Form):
    doctor = forms.ChoiceField(
        label="Select a Doctor",
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'doctor-radio'}),
    )
    
    def __init__(self, *args, **kwargs):
        doctors = kwargs.pop('doctors', [])
        super().__init__(*args, **kwargs)
        
        # Create choices from doctors queryset
        self.fields['doctor'].choices = [(doctor.user_id, str(doctor)) for doctor in doctors]
        
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.form_tag = False
        self.helper.disable_csrf = True

class AppointmentTypeForm(forms.Form):
    APPOINTMENT_TYPES = [
        ('video', 'Video Consultation'),
        ('clinic', 'In-Clinic Visit'),
        ('emergency', 'Emergency Consultation'),
    ]
    
    appointment_type = forms.ChoiceField(
        label="Select Appointment Type",
        choices=APPOINTMENT_TYPES,
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'appointment-type-radio'}),
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.form_tag = False
        self.helper.disable_csrf = True

class DateSelectionForm(forms.Form):
    appointment_date = forms.DateField(
        label="Select Date",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'id_appointment_date'}),
        required=True,
        help_text='Appointments are available for the next 30 days'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Field('appointment_date'),
        )

class TimeSlotForm(forms.Form):
    time_slot = forms.ChoiceField(
        label="Available Time Slots",
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'time-slot-radio'}),
    )
    
    def __init__(self, *args, **kwargs):
        time_slots = kwargs.pop('time_slots', [])
        super().__init__(*args, **kwargs)
        
        # Create choices from time slots
        self.fields['time_slot'].choices = [(slot, slot) for slot in time_slots]
        
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.form_tag = False
        self.helper.disable_csrf = True

class ReasonForm(forms.Form):
    appointment_reason = forms.CharField(
        label="Reason for Visit",
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Please describe the reason for your appointment...',
            'class': 'form-control',
            'id': 'id_appointment_reason'
        }),
        required=True,
        help_text='Providing details helps the doctor prepare for your consultation'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Field('appointment_reason'),
        )

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 
                 'phone_number', 'date_of_birth', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-6'),
                Column('password2', css_class='form-group col-md-6'),
            ),
            Row(
                Column('phone_number', css_class='form-group col-md-6'),
                Column('date_of_birth', css_class='form-group col-md-6'),
            ),
            'address',
            Submit('submit', 'Create Account', css_class='btn-primary w-100')
        )

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address',
            'id': 'id_username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Password',
            'id': 'id_password'
        })
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Extract the request argument if provided
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Sign In', css_class='btn-primary w-100')
        )

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].widget.attrs.update({'class': 'form-select'})
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'doctor',
            Row(
                Column('date', css_class='form-group col-md-6'),
                Column('time', css_class='form-group col-md-6'),
            ),
            'reason',
            Submit('submit', 'Book Appointment', css_class='btn-primary')
        )

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'rating',
            'comments',
            Submit('submit', 'Submit Feedback', css_class='btn-primary')
        )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

class MultiStepRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        })
    )
    role = forms.ChoiceField(
        choices=[('', 'Select your role'), ('patient', 'Patient'), ('doctor', 'Doctor')],
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
        })
    )
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number',
        })
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        })
    )
    gender = forms.ChoiceField(
        choices=[('', 'Select gender'), ('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    agree_to_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                 'phone_number', 'date_of_birth', 'gender', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the default username field since we're using email
        self.fields.pop('username', None)
        
        # Initialize crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'crispy-form'
        self.helper.form_show_labels = False  # Hide labels since we use icons and placeholders
        
        # Ensure all fields have proper CSS classes
        for field_name, field in self.fields.items():
            if field_name in ['role', 'gender']:
                field.widget.attrs.update({'class': 'form-select'})
            elif field_name == 'agree_to_terms':
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        # Custom password validation
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one digit.")
        
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        
        if not any(char.islower() for char in password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.gender = self.cleaned_data['gender']

        # Set username as email for simplicity
        user.username = self.cleaned_data['email']

        # Set role
        role = self.cleaned_data['role']
        if role == 'doctor':
            user.is_doctor = True
            user.is_patient = False
        else:
            user.is_patient = True
            user.is_doctor = False

        if commit:
            user.save()
            
            # If user is a doctor, create a Doctor profile
            if user.is_doctor:
                Doctor.objects.create(
                    user=user,
                    specialization='General',  # Default value
                    experience=0  # Default value
                )
        return user

    def clean(self):
        cleaned_data = super().clean()
        # Add any additional validation here
        return cleaned_data
