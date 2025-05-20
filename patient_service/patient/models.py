from django.db import models

class MedicalRecord(models.Model):
    patient_id = models.IntegerField()  # Lưu id user patient từ AuthService
    record_date = models.DateField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"MedicalRecord {self.id} for patient {self.patient_id}"

class Appointment(models.Model):
    patient_id = models.IntegerField()  # id user patient từ AuthService
    doctor_id = models.IntegerField()
    appointment_time = models.DateTimeField()
    status = models.CharField(max_length=20, default='pending')  # pending, confirmed, rejected

    def __str__(self):
        return f"Appointment {self.id} patient {self.patient_id} doctor {self.doctor_id}"
