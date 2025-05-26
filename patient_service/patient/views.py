import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import MedicalRecord, Appointment
from .serializers import (
    MedicalRecordSerializer,
    AppointmentSerializer,
    AppointmentCreateSerializer,
)
from rest_framework.permissions import AllowAny

AUTH_SERVICE_USERINFO_URL = "http://127.0.0.1:8000/api/auth/accounts/auth/profile/"


class PatientBaseView(APIView):
    permission_classes = [AllowAny]

    def get_patient_info(self, request):
        # Lấy token từ header client gửi lên
        auth_header = request.headers.get("Authorization")
        print(f"Authorization header: {auth_header}")
        if not auth_header:
            print(f"Authorization header: {auth_header}")
            return None, Response(
                {"detail": "Authorization header missing"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Gọi AuthService để lấy thông tin user
        try:
            resp = requests.get(
                AUTH_SERVICE_USERINFO_URL,
                headers={"Authorization": auth_header},
                timeout=5,
            )
            if resp.status_code != 200:
                return None, Response(
                    {"detail": "Failed to get user info from AuthService"},
                    status=resp.status_code,
                )

            user_data = resp.json()

            # Kiểm tra role phải là patient mới được truy cập
            if user_data.get("role") != "patient":
                return None, Response(
                    {"detail": "User is not a patient"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            return user_data, None

        except requests.RequestException as e:
            return None, Response(
                {"detail": "Error contacting AuthService", "error": str(e)}, status=500
            )


class PatientInfoView(PatientBaseView):
    def get(self, request):
        user_data, error_response = self.get_patient_info(request)
        if error_response:
            return error_response

        # Trả lại thông tin user lấy từ AuthService
        return Response(user_data)


class MedicalRecordsView(PatientBaseView):
    def get(self, request):
        user_data, error_response = self.get_patient_info(request)
        if error_response:
            return error_response

        patient_id = user_data["id"]
        records = MedicalRecord.objects.filter(patient_id=patient_id)
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)


class AppointmentListView(PatientBaseView):
    def get(self, request):
        user_data, error_response = self.get_patient_info(request)
        if error_response:
            return error_response

        patient_id = user_data["id"]
        appointments = Appointment.objects.filter(patient_id=patient_id)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_data, error_response = self.get_patient_info(request)
        if error_response:
            return error_response

        patient_id = user_data["id"]
        serializer = AppointmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            appointment = Appointment.objects.create(
                patient_id=patient_id,
                doctor_id=serializer.validated_data["doctor_id"],
                appointment_time=serializer.validated_data["appointment_time"],
                status="pending",
            )
            return Response(
                AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
