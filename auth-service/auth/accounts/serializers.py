from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from .models import PatientProfile, DoctorProfile, PharmacistProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role', 'phone', 'address')
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = True
        return user

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['date_of_birth', 'insurance_number']

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['specialty', 'license_number']

class PharmacistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacistProfile
        fields = ['license_number', 'pharmacy_name']

class UserProfileSerializer(serializers.ModelSerializer):
    
    profile = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email', 'phone', 'role', 'address',
                  'profile']
    def get_profile(self, obj):
        if obj.role == 'patient':
            profile = getattr(obj, 'patient_profile', None)
            if profile:
                return PatientProfileSerializer(profile).data
        elif obj.role == 'doctor':
            profile = getattr(obj, 'doctor_profile', None)
            if profile:
                return DoctorProfileSerializer(profile).data
        elif obj.role == 'pharmacist':
            profile = getattr(obj, 'pharmacist_profile', None)
            if profile:
                return PharmacistProfileSerializer(profile).data
        return None
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)  # Lấy data từ key 'profile'

        print("Profile data:", profile_data)
        # Cập nhật các field user bình thường
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Cập nhật profile tương ứng theo role
        if profile_data:
            profile = getattr(instance, f"{instance.role}_profile", None)
            if profile:
                for attr, value in profile_data.items():
                    setattr(profile, attr, value)
                profile.save()
            else:
                # Nếu chưa có profile thì tạo mới
                ProfileModel = {
                    'patient': PatientProfile,
                    'doctor': DoctorProfile,
                    'pharmacist': PharmacistProfile,
                }[instance.role]
                ProfileModel.objects.create(user=instance, **profile_data)

        return instance