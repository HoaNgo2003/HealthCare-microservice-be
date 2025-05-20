# medical/models.py

from django.db import models

class MedicalRecord(models.Model):
    patient_id = models.CharField(max_length=100)  # ID từ AuthService
    doctor_id = models.CharField(max_length=100)   # ID từ DoctorService
    description = models.TextField()
    diagnosis = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Medical Record for Patient {self.patient_id}"

class Prescription(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    doctor_id = models.CharField(max_length=100)
    patient_id = models.CharField(max_length=100)
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    prescribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription {self.medicine_name} for Patient {self.patient_id}"
