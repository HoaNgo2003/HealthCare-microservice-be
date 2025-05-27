from django.db import models

class MedicalRecord(models.Model):
    patient_id = models.IntegerField()  # Lưu id user patient từ AuthService
    record_date = models.DateField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"MedicalRecord {self.id} for patient {self.patient_id}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    patient_id = models.CharField(max_length=100)  # ID bệnh nhân từ Patient Service (hoặc AuthService)
    doctor_id = models.CharField(max_length=100)   # ID bác sĩ (có thể từ Doctor Service)
    appointment_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
