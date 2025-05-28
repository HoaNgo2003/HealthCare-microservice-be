import requests

MEDICAL_SERVICE_BASE_URL = "http://doctor-service:8006/api"

def get_medical_records_by_patient(patient_id):
    url = f"{MEDICAL_SERVICE_BASE_URL}/medical-records/patient/{patient_id}/"
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
    except requests.RequestException as e:
        print(f"Error fetching medical records: {e}")
        return None

def get_prescriptions_by_patient(patient_id):
    url = f"{MEDICAL_SERVICE_BASE_URL}/prescriptions/patient/{patient_id}/"
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
    except requests.RequestException as e:
        print(f"Error fetching prescriptions: {e}")
        return None
