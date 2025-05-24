from rest_framework import serializers
from .models import Prescription, DrugDistribution
import requests
class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

class DrugDistributionSerializer(serializers.ModelSerializer):
    doctor_info = serializers.SerializerMethodField()
    drug_info = serializers.SerializerMethodField()

    class Meta:
        model = DrugDistribution
        fields = ['id', 'doctor_id', 'drug_type_id', 'quantity', 'doctor_info', 'drug_info']

    def get_doctor_info(self, obj):
        try:
            resp = requests.get(f"http://127.0.0.1:8000/api/accounts/auth/users/{obj.doctor_id}/")
            if resp.status_code == 200:
                return resp.json()
            else:
                return None
        except Exception:
            return None

    def get_drug_info(self, obj):
        try:
            resp = requests.get(f"http://127.0.0.1:8004/api/pharmacist/{obj.drug_type_id}/")
            if resp.status_code == 200:
                return resp.json()
            else:
                return None
        except Exception:
            return None
        