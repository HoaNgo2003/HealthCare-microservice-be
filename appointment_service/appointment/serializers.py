from rest_framework import serializers
from .models import Appointment
import requests
PROFILE_URL = 'http://127.0.0.1:8000/api/accounts/auth/users/'
class AppointmentSerializer(serializers.ModelSerializer):
    doctor_info = serializers.SerializerMethodField()
    patient_info = serializers.SerializerMethodField()
    class Meta:
        model = Appointment
        fields = ['id', 'appointment_time', 'status', 'notes', 'doctor_info', 'patient_info']
    def get_doctor_info(self, obj):
        try:
            response = requests.get(f"{PROFILE_URL}{obj.doctor_id}/")
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.RequestException as e:
            return None
    def get_patient_info(self, obj):
        try:
            response = requests.get(f"{PROFILE_URL}{obj.patient_id}/")
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.RequestException as e:
            return None

class AppointmentStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Appointment.STATUS_CHOICES)

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'  # Cho phép cập nhật tất cả các trường
        