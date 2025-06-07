from django.contrib import admin
from .models import User, PatientProfile, DoctorProfile, PharmacistProfile


# Hiển thị User trong trang Admin
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "full_name", "email", "role", "phone", "address")
    search_fields = ["username", "email", "full_name"]
    list_filter = ("role",)
    ordering = ("username",)


# Đăng ký User model
admin.site.register(User, UserAdmin)
