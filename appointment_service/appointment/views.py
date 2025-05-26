from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Appointment
from .serializers import (
    AppointmentSerializer,
    AppointmentStatusUpdateSerializer,
    AppointmentUpdateSerializer,
)
import requests

AUTH_SERVICE_USERINFO_URL = "http://127.0.0.1:8000/api/auth/accounts/auth/profile/"  # sửa url authservice phù hợp


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
