"""
Simple script to create a test doctor in the database.
Run this with: python manage.py shell < create_test_doctor.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Medweb.settings')
django.setup()

from myapp.models import User, Doctor

# Create a doctor user if it doesn't exist
username = "dr_smith"
if not User.objects.filter(username=username).exists():
    user = User.objects.create_user(
        username=username,
        email="dr.smith@hospital.com",
        password="doctor123",
        first_name="John",
        last_name="Smith",
        is_doctor=True,
        is_patient=False
    )
    
    # Create doctor profile
    doctor = Doctor.objects.create(
        user=user,
        specialization="General Physician",
        experience=10,
        available=True
    )
    
    print(f"✅ Doctor created successfully!")
    print(f"   Username: {username}")
    print(f"   Password: doctor123")
    print(f"   Name: Dr. {user.first_name} {user.last_name}")
    print(f"   Specialization: {doctor.specialization}")
else:
    print(f"⚠️  Doctor with username '{username}' already exists!")

# Show total doctors
total_doctors = Doctor.objects.count()
print(f"\nTotal doctors in database: {total_doctors}")
