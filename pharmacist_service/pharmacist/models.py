 
from django.db import models

class Prescription(models.Model):
    name = models.CharField(max_length=255)  # Tên thuốc
    quantity = models.PositiveIntegerField()  # Số lượng
    expiry_date = models.DateField()  # Hạn dùng

    def __str__(self):
        return f"{self.name} - {self.quantity} - {self.expiry_date}"
      
class DrugDistribution(models.Model):
    doctor_id = models.IntegerField()      # id bác sĩ (từ microservice)
    drug_type_id = models.IntegerField()   # id loại thuốc (từ bảng Thuốc hoặc microservice)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Doctor {self.doctor_id} dispensed drug {self.drug_type_id} x {self.quantity}"