from rest_framework import serializers
from .models import MedicalRecord, Appointment

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class AppointmentCreateSerializer(serializers.Serializer):
    doctor_id = serializers.IntegerField()
    appointment_time = serializers.DateTimeField()
