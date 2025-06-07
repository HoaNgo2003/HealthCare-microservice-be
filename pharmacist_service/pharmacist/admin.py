from django.contrib import admin
from .models import Prescription, DrugDistribution


# Hiển thị Prescription trong trang Admin
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "quantity",
        "expiry_date",
    )  # Các trường sẽ hiển thị trong bảng quản lý
    search_fields = ["name"]  # Cho phép tìm kiếm theo tên thuốc
    list_filter = ("expiry_date",)  # Lọc theo ngày hết hạn
    ordering = ("name",)  # Sắp xếp theo tên thuốc


# Đăng ký Prescription model
admin.site.register(Prescription, PrescriptionAdmin)


# Hiển thị DrugDistribution trong trang Admin
class DrugDistributionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "doctor_id",
        "drug_type_id",
        "quantity",
    )  # Các trường sẽ hiển thị trong bảng quản lý
    search_fields = [
        "doctor_id",
        "drug_type_id",
    ]  # Cho phép tìm kiếm theo doctor_id và drug_type_id
    list_filter = ("doctor_id",)  # Lọc theo bác sĩ
    ordering = ("doctor_id",)  # Sắp xếp theo doctor_id


# Đăng ký DrugDistribution model
admin.site.register(DrugDistribution, DrugDistributionAdmin)
