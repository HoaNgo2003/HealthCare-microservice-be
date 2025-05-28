import requests

PATIENT_SERVICE_BASE_URL = "http://patient-service:8002/api"


def get_appointments_by_doctor(doctor_id):
    url = f"{PATIENT_SERVICE_BASE_URL}/patients/appointments/doctor/{doctor_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException as e:
        print(f"Error fetching doctor appointments: {e}")
        return None


def update_appointment_status(appointment_id, new_status):
    url = f"{PATIENT_SERVICE_BASE_URL}/patients/appointments/{appointment_id}/status"
    try:
        response = requests.put(url, json={"status": new_status})
        return response.json() if response.status_code == 200 else None
    except requests.RequestException as e:
        print(f"Error updating appointment status: {e}")
        return None


def delete_appointment(appointment_id):
    url = f"{PATIENT_SERVICE_BASE_URL}/delete/{appointment_id}"
    try:
        response = requests.delete(url)
        return response.status_code == 204
    except requests.RequestException as e:
        print(f"Error deleting appointment: {e}")
        return False
