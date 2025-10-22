from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Appointment, Feedback, Doctor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML, Field

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    role = forms.ChoiceField(choices=[('patient', 'Patient'), ('doctor', 'Doctor')], required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
            ),
            'role',
            Submit('submit', 'Register', css_class='btn btn-primary w-100')
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        role = self.cleaned_data['role']
        if role == 'doctor':
            user.is_doctor = True
            user.is_patient = False
        else:
            user.is_patient = True
            user.is_doctor = False

        if commit:
            user.save()
            # Create doctor profile if role is doctor
            if role == 'doctor':
                Doctor.objects.create(user=user, specialization="General", experience=0)
        return user

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'symptoms']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'symptoms': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Describe your symptoms...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(available=True)
        self.fields['doctor'].required = False
        self.fields['doctor'].empty_label = "Select a doctor (optional)"
        self.fields['doctor'].widget.attrs.update({'class': 'form-control'})
        
        # Add crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('doctor', css_class='mb-3'),
            Field('date', css_class='mb-3'),
            Field('symptoms', css_class='mb-3'),
            Submit('submit', 'Submit Appointment', css_class='btn btn-primary w-100')
        )

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your feedback here...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'message',
            Submit('submit', 'Submit Feedback', css_class='btn btn-primary w-100')
        )

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your password'
        }),
        label="Password"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'form-label fw-bold'
        self.helper.field_class = 'mb-3'
        
        self.helper.layout = Layout(
            HTML('<h2 class="text-center mb-4">Sign In</h2>'),
            Field('username', placeholder='Enter your username'),
            Field('password', placeholder='Enter your password'),
            Div(
                Submit('submit', 'Sign In', css_class='btn btn-primary w-100 btn-lg'),
                css_class='form-group mt-4'
            ),
            HTML('<p class="text-center mt-3">Don\'t have an account? <a href="/register/">Register here</a></p>')
        )
