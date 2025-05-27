import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import MedicalRecord, Appointment
from .serializers import (
    AppointmentSerializer,
)
from rest_framework.permissions import AllowAny
from .serializers import (
    AppointmentSerializer,
    AppointmentStatusUpdateSerializer,
    AppointmentUpdateSerializer,
)
from .patientservice import get_medical_records_by_patient, get_prescriptions_by_patient
AUTH_SERVICE_USERINFO_URL = "http://auth-service:8000/api/auth/accounts/auth/profile/" #test



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


 
    def get(self, request):
        user_data, error_response = self.get_patient_info(request)
        if error_response:
            return error_response

        # Trả lại thông tin user lấy từ AuthService
        return Response(user_data)
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
class AppointmentView(APIView):
    permission_classes = [permissions.AllowAny]  # test tạm, production cần auth token

    def get_patient_id(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None, Response(
                {"detail": "Missing Authorization header"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            resp = requests.get(
                AUTH_SERVICE_USERINFO_URL, headers={"Authorization": auth_header}
            )
            if resp.status_code != 200:
                return None, Response(
                    {"detail": "Failed to get user info from AuthService"},
                    status=resp.status_code,
                )
            user_data = resp.json()
            if user_data.get("role") != "patient":
                return None, Response(
                    {"detail": "User is not patient"}, status=status.HTTP_403_FORBIDDEN
                )
            return user_data.get("id"), None
        except Exception as e:
            return None, Response(
                {"detail": "Error contacting AuthService", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request):
        patient_id, err_response = self.get_patient_id(request)
        if err_response:
            return err_response

        appointments = Appointment.objects.filter(patient_id=patient_id).order_by(
            "-appointment_time"
        )
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request):
        patient_id, err_response = self.get_patient_id(request)
        notes = request.data.get("notes", "")
        if err_response:
            return err_response

        doctor_id = request.data.get("doctor_id")
        appointment_time = request.data.get("appointment_time")

        if not doctor_id or not appointment_time:
            return Response(
                {"detail": "doctor_id and appointment_time are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment = Appointment.objects.create(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_time=appointment_time,
            status="pending",
            notes=notes,
        )
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AppointmentStatusUpdateView(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response(
                {"detail": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AppointmentStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            appointment.status = serializer.validated_data["status"]
            appointment.save()
            return Response({"detail": "Status updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response(
                {"detail": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def delete(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.delete()
            return Response(
                {"detail": "Appointment deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        except Appointment.DoesNotExist:
            return Response(
                {"detail": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND
            )


class GetListAppointmentByDoctorId(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, doctor_id):
        appointments = Appointment.objects.filter(doctor_id=doctor_id).order_by(
            "-appointment_time"
        )
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


class GetListAppointmentByPatientId(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, patient_id):
        appointments = Appointment.objects.filter(patient_id=patient_id).order_by(
            "-appointment_time"
        )
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


class GetListAppointmentByStatus(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, status):
        appointments = Appointment.objects.filter(status=status).order_by(
            "-appointment_time"
        )
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


class AppointmentUpdateView(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response(
                {"detail": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AppointmentUpdateSerializer(
            appointment, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Appointment updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDeleteView(APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.delete()
            return Response(
                {"detail": "Appointment deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Appointment.DoesNotExist:
            return Response(
                {"detail": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND
            )


class PatientMedicalRecordsView(APIView):
    def get(self, request, patient_id):
        data = get_medical_records_by_patient(patient_id)
        if data is not None:
            return Response(data)
        return Response({"error": "Failed to fetch medical records"}, status=status.HTTP_502_BAD_GATEWAY)

class PatientPrescriptionsView(APIView):
    def get(self, request, patient_id):
        data = get_prescriptions_by_patient(patient_id)
        if data is not None:
            return Response(data)
        return Response({"error": "Failed to fetch prescriptions"}, status=status.HTTP_502_BAD_GATEWAY)