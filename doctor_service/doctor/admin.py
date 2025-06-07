from django.contrib import admin
from .models import MedicalRecord, Prescription


class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 1  # Số dòng mẫu khi thêm mới Prescription


class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient_id",
        "doctor_id",
        "created_at",
    )  # Hiển thị các trường này trong danh sách
    search_fields = (
        "patient_id",
        "doctor_id",
    )  # Cho phép tìm kiếm theo patient_id và doctor_id
    list_filter = ("created_at",)  # Bộ lọc theo ngày tạo
    inlines = [
        PrescriptionInline
    ]  # Hiển thị Prescription như một phần trong MedicalRecord


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "medical_record",
        "medicine_name",
        "quantity",
        "prescribed_at",
    )  # Hiển thị các trường này trong danh sách
    search_fields = (
        "medicine_name",
        "patient_id",
    )  # Tìm kiếm theo medicine_name và patient_id
    list_filter = ("prescribed_at",)  # Bộ lọc theo ngày kê đơn


# Đăng ký model vào Admin
admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
