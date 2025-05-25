# medical/serializers.py

from rest_framework import serializers
from .models import MedicalRecord, Prescription
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)
PROFILE_URL = getattr(
    settings, "PROFILE_URL", "http://127.0.0.1:8000/api/accounts/auth/users/"
)


def fetch_user_info(user_id, token=None):
    url = f"{PROFILE_URL}{user_id}/"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.get(url, headers=headers)
        logger.debug(f"GET {url} -> {response.status_code}")
        logger.debug(f"Response content: {response.text}")

        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
    return None


class MedicalRecordSerializer(serializers.ModelSerializer):
    doctor_info = serializers.SerializerMethodField()
    patient_info = serializers.SerializerMethodField()

    class Meta:
        model = MedicalRecord
        fields = [
            "id",
            "created_at",
            "description",
            "diagnosis",
            "doctor_info",
            "patient_info",
            "patient_id",
            "doctor_id",
        ]

    def get_doctor_info(self, obj):
        token = self.context.get("token")
        print(obj.doctor_id)
        return fetch_user_info(obj.doctor_id, token)

    def get_patient_info(self, obj):
        token = self.context.get("token")
        print(obj.patient_id)
        return fetch_user_info(obj.patient_id, token)


class PrescriptionSerializer(serializers.ModelSerializer):
    doctor_info = serializers.SerializerMethodField()
    patient_info = serializers.SerializerMethodField()
    medical_record_info = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = [
            "id",
            "prescribed_at",
            "medical_record",
            "medical_record_info",
            "dosage",
            "instructions",
            "doctor_info",
            "patient_info",
            "medicine_name",
            "doctor_id",
            "patient_id",
            "quantity",
        ]

    def get_doctor_info(self, obj):
        token = self.context.get("token")
        return fetch_user_info(obj.doctor_id, token)

    def get_patient_info(self, obj):
        token = self.context.get("token")
        return fetch_user_info(obj.patient_id, token)

    def get_medical_record_info(self, obj):
        token = self.context.get("token")
        return MedicalRecordSerializer(
            obj.medical_record, context={"token": token}
        ).data
