from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('pharmacist', 'Pharmacist'),
    )

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    address = models.TextField(blank=True)

    REQUIRED_FIELDS = ['email', 'full_name', 'phone', 'role']
    USERNAME_FIELD = 'username'  # bạn có thể đổi sang 'email' nếu muốn login bằng email

    def __str__(self):
        return f"{self.username} ({self.role})"

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    insurance_number = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"PatientProfile of {self.user.username}"

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100)

    def __str__(self):
        return f"DoctorProfile of {self.user.username}"

class PharmacistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pharmacist_profile')
    license_number = models.CharField(max_length=100)
    pharmacy_name = models.CharField(max_length=100)

    def __str__(self):
        return f"PharmacistProfile of {self.user.username}"
